from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from issue.models import Issue
from issue.forms import IssueForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issue_list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['issues_list'] = Issue.objects.all()
        else:
            context['issues_list'] = Issue.objects.filter(assignee=self.request.user)
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


class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = "issue/issue_detail.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


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
    fields = ['title', 'description', 'priority', 'assignee', 'state', 'expired_date']
    template_name_suffix = '_update_form'

    def get_form(self):
        form = super().get_form()
        form.fields['title'].label = 'Titolo'
        form.fields['description'].label = 'Descrizione'
        form.fields['priority'].label = 'Priorità'
        form.fields['assignee'].label = 'Assegnatario'
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
