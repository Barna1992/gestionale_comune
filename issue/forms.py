from django import forms
from gestione_comune import settings
from .models import Issue, Comment
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
        self.fields['expired_date'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['expired_date'].widget.attrs.update({'class': 'datepicker'})
        assignee = [i for i in self.fields['assignee'].choices]
        assignee.append((1000, 'Tutti'))
        self.fields['assignee'] = forms.MultipleChoiceField(
            choices=assignee,
            widget=forms.CheckboxSelectMultiple,
            label=("Assegnatario")
        )

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        user_id = [i for i in cleaned_data['assignee']]
        if '1000' in user_id:
            cleaned_data['assignee'] = User.objects.all()
        else:
            cleaned_data['assignee'] = [User.objects.get(id=i) for i in user_id]
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'post', 'name')
        labels = {
            'body': 'il mio commento',
            'post': '',
            'name': '',
        }
