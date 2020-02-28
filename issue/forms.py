from django import forms

from .models import Issue
from django.contrib.auth.models import User

class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ('title', 'description', 'assignee', 'state', 'priority', 'expired_date')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Titolo"
        self.fields['description'].label = "Descrizione"
        self.fields['state'].label = "Stato"
        self.fields['priority'].label = "Priorità"
        self.fields['expired_date'].label = "Termine"
        self.fields['expired_date'].widget.attrs.update({'class': 'datepicker'})
        self.fields['assignee'] = forms.MultipleChoiceField(
            choices=self.fields['assignee'].choices,
            widget=forms.CheckboxSelectMultiple,
            label=("Assegnatario")
        )

    def clean(self):
        cleaned_data = super().clean()
        user_id = [i for i in cleaned_data['assignee']]
        cleaned_data['assignee'] = [User.objects.get(id=i) for i in user_id]
        return cleaned_data