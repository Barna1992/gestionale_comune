from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from .forms import UserCreateForm, UserEditForm


class SuperuserRequiredMixin(LoginRequiredMixin):
    """Returns 403 if the user is not a superuser."""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated and not request.user.is_superuser:
            raise PermissionDenied
        return response


class SignUpView(SuperuserRequiredMixin, View):
    form_class = UserCreateForm
    template_name = 'registration/sign_up.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utente creato con successo.')
            return redirect('accounts:user_list')
        return render(request, self.template_name, {'form': form})


class UserListView(SuperuserRequiredMixin, ListView):
    model = User
    template_name = 'registration/user_list.html'
    context_object_name = 'users'
    ordering = ['username']


class UserCreateView(SuperuserRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Utente "{self.object.username}" creato con successo.')
        return response


class UserEditView(SuperuserRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Utente "{self.object.username}" modificato con successo.')
        return response


class UserToggleActiveView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, 'Non puoi disattivare te stesso.')
            return redirect('accounts:user_list')
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        status = 'attivato' if user.is_active else 'disattivato'
        messages.success(request, f'Utente "{user.username}" {status}.')
        return redirect('accounts:user_list')
