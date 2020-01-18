from django import forms

from .models import Issue

class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = ('title', 'description', 'assignee', 'state', 'priority', 'expired_date')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Titolo"
        self.fields['description'].label = "Descrizione"
        self.fields['assignee'].label = "Assegnatario"
        self.fields['state'].label = "Stato"
        self.fields['priority'].label = "Priorità"
        self.fields['expired_date'].label = "Termine"
        self.fields['expired_date'].widget.attrs.update({'class': 'datepicker'})
