from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from issue.models import Issue
from issue.forms import IssueForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.db.models import Q

class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issue_list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['issues_list'] = Issue.objects.all()
        else:
            context['issues_list'] = Issue.objects.filter(Q(assignee=self.request.user) | Q(cc=self.request.user))
        context['user'] = self.request.user
        filters = ['assignee', 'priority', 'state', 'date', 'expired_date']
        for f in filters:
            if f in self.request.GET:
                context['issues_list'] = context['issues_list'].order_by(f)
            if '-{}'.format(f) in self.request.GET:
                context['issues_list'] = context['issues_list'].order_by('-{}'.format(f))
        context['all_user_number'] = User.objects.all().count()
        context['new_issue'] = context['issues_list'].filter(state=1).count()
        return context


class IssueDetailView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = "issue/issue_detail.html"
    model = Issue
    form_class = CommentForm

    def get_success_url(self):
        return reverse('issue-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = CommentForm(initial={'post': self.object, 'name': self.request.user})
        context['cc_only'] = (self.request.user in self.object.cc.all()) and \
                             not (self.request.user in self.object.assignee.all())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class MainView(LoginRequiredMixin, TemplateView):
    template_name = "issue/index.html"


class IssueFormView(LoginRequiredMixin, FormView):
    template_name = 'issue/issue_create.html'
    form_class = IssueForm
    success_url = '/issue/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'create_issue': True})
        return context

class IssueEditFormView(LoginRequiredMixin, UpdateView):
    model = Issue
    fields = ['title', 'description', 'priority', 'assignee','cc', 'state', 'expired_date']
    template_name_suffix = '_update_form'

    def get_form(self):
        form = super().get_form()
        form.fields['title'].label = 'Titolo'
        form.fields['description'].label = 'Descrizione'
        form.fields['priority'].label = 'Priorità'
        form.fields['assignee'].label = 'Assegnatario'
        form.fields['cc'].label = 'In CC'
        form.fields['state'].label = 'Stato'
        form.fields['expired_date'].label = 'Termine'
        return form


class IssueEditStateFormView(LoginRequiredMixin, UpdateView):
    model = Issue
    fields = ['state']
    template_name_suffix = '_update_form'

    def get_form(self):
        form = super().get_form()
        form.fields['state'].label = 'Stato'
        return form

class IssueDeleteFormView(LoginRequiredMixin, DeleteView):
    model = Issue
    success_url = reverse_lazy('base')
