from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label='Nome')
    last_name = forms.CharField(max_length=30, required=False, label='Cognome')
    email = forms.EmailField(required=False, label='Email')
    is_active = forms.BooleanField(required=False, initial=True, label='Attivo')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_active']


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Nome')
    last_name = forms.CharField(max_length=30, required=False, label='Cognome')
    email = forms.EmailField(required=False, label='Email')
    is_active = forms.BooleanField(required=False, label='Attivo')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
