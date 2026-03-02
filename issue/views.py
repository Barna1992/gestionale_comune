import json
from datetime import timedelta

from django import forms as django_forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import FormView

from .forms import AttachmentForm, CommentForm, IssueForm
from .models import Attachment, Category, Comment, Issue


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'issue/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        if self.request.user.is_superuser:
            issues = Issue.objects.all()
        else:
            issues = Issue.objects.filter(
                Q(assignee=self.request.user) | Q(cc=self.request.user)
            ).distinct()

        context['total_issues'] = issues.count()
        context['open_issues'] = issues.exclude(state=3).count()
        context['resolved_issues'] = issues.filter(state=3).count()
        context['high_priority'] = issues.filter(priority=3).exclude(state=3).count()
        context['expired_issues'] = issues.filter(
            expired_date__lt=now.date(),
        ).exclude(state=3).count()

        context['recent_issues'] = issues.order_by('-created_at')[:10]
        context['upcoming_deadlines'] = issues.filter(
            expired_date__gte=now.date(),
            expired_date__lte=now.date() + timedelta(days=7),
        ).exclude(state=3).order_by('expired_date')

        # Data for charts
        state_data = issues.values('state').annotate(count=Count('id'))
        state_labels = dict(Issue._meta.get_field('state').choices)
        context['chart_state_labels'] = json.dumps(
            [str(state_labels.get(s['state'], '')) for s in state_data]
        )
        context['chart_state_data'] = json.dumps([s['count'] for s in state_data])

        category_data = issues.exclude(category__isnull=True).values(
            'category__name',
        ).annotate(count=Count('id')).order_by('-count')
        context['chart_category_labels'] = json.dumps(
            [c['category__name'] for c in category_data]
        )
        context['chart_category_data'] = json.dumps([c['count'] for c in category_data])

        priority_data = issues.values('priority').annotate(count=Count('id'))
        priority_labels = dict(Issue._meta.get_field('priority').choices)
        context['chart_priority_labels'] = json.dumps(
            [str(priority_labels.get(p['priority'], '')) for p in priority_data]
        )
        context['chart_priority_data'] = json.dumps([p['count'] for p in priority_data])

        return context


class IssueListView(LoginRequiredMixin, ListView):
    template_name = 'issue/issue_list.html'
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            qs = Issue.objects.all()
        else:
            qs = Issue.objects.filter(
                Q(assignee=self.request.user) | Q(cc=self.request.user)
            ).distinct()

        filters = ['assignee', 'priority', 'state', 'created_at', 'expired_date']
        for f in filters:
            if f in self.request.GET:
                qs = qs.order_by(f)
            if f'-{f}' in self.request.GET:
                qs = qs.order_by(f'-{f}')

        context['issues_list'] = qs.select_related('category', 'owner').prefetch_related('assignee', 'cc')
        context['all_user_number'] = User.objects.count()
        context['new_issue'] = qs.filter(state=1).count()
        return context


class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = 'issue/issue_detail.html'
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cc_only'] = (
            self.request.user in self.object.cc.all()
            and self.request.user not in self.object.assignee.all()
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_type = request.POST.get('form_type', 'comment')

        if form_type == 'attachment':
            return self._handle_attachment(request)
        else:
            return self._handle_comment(request)

    def _handle_comment(self, request):
        body = request.POST.get('body', '').strip()
        if body:
            comment = Comment.objects.create(
                post=self.object,
                name=request.user,
                body=body,
            )
            from .notifications import notify_comment_added
            notify_comment_added(comment, request)
            messages.success(request, 'Commento aggiunto.')
        else:
            messages.error(request, 'Il commento non può essere vuoto.')
        return redirect('issue-detail', pk=self.object.pk)

    def _handle_attachment(self, request):
        if not request.user.is_superuser:
            messages.error(request, 'Non hai i permessi per caricare allegati.')
            return redirect('issue-detail', pk=self.object.pk)

        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            if uploaded_file.size > 10 * 1024 * 1024:
                messages.error(request, 'Il file non può superare i 10 MB.')
            else:
                Attachment.objects.create(
                    issue=self.object,
                    file=uploaded_file,
                    uploaded_by=request.user,
                    description=request.POST.get('att_description', ''),
                )
                messages.success(request, 'Allegato caricato.')
        else:
            messages.error(request, 'Nessun file selezionato.')
        return redirect('issue-detail', pk=self.object.pk)


class IssueFormView(LoginRequiredMixin, FormView):
    template_name = 'issue/issue_create.html'
    form_class = IssueForm
    success_url = reverse_lazy('base')

    def form_valid(self, form):
        issue = form.save()
        issue.owner = self.request.user
        issue.save()

        # Handle attachment upload on creation
        attachment = self.request.FILES.get('attachment')
        if attachment:
            if attachment.size <= 10 * 1024 * 1024:
                Attachment.objects.create(
                    issue=issue,
                    file=attachment,
                    uploaded_by=self.request.user,
                )

        from .notifications import notify_issue_assigned
        notify_issue_assigned(issue, self.request)
        messages.success(self.request, f'Segnalazione "#{issue.pk} - {issue.title}" creata.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_issue'] = True
        return context


class IssueEditFormView(LoginRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm
    template_name_suffix = '_update_form'


class IssueEditStateFormView(LoginRequiredMixin, UpdateView):
    model = Issue
    fields = ['state']
    template_name_suffix = '_update_form'

    def get_form(self):
        form = super().get_form()
        form.fields['state'].label = 'Stato'
        return form

    def form_valid(self, form):
        old_state = Issue.objects.get(pk=self.object.pk).state
        response = super().form_valid(form)
        new_state = self.object.state
        if old_state != new_state:
            from .notifications import notify_state_changed
            notify_state_changed(self.object, old_state, new_state, self.request.user, self.request)
        return response


class IssueDeleteFormView(LoginRequiredMixin, DeleteView):
    model = Issue
    success_url = reverse_lazy('base')


class AttachmentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        attachment = get_object_or_404(Attachment, pk=pk)
        issue_pk = attachment.issue.pk
        if request.user.is_superuser:
            attachment.file.delete(save=False)
            attachment.delete()
            messages.success(request, 'Allegato eliminato.')
        else:
            messages.error(request, 'Non hai i permessi per eliminare allegati.')
        return redirect('issue-detail', pk=issue_pk)


# Keep for backward compat - now redirects to dashboard
class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'issue/index.html'
