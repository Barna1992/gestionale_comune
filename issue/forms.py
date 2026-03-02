from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Attachment, Comment, Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'description', 'category', 'assignee', 'cc', 'state', 'priority', 'expired_date')
        error_messages = {
            'title': {
                'required': 'Il titolo è obbligatorio.',
                'max_length': 'Il titolo non può superare i 200 caratteri.',
            },
            'description': {
                'required': 'La descrizione è obbligatoria.',
            },
            'assignee': {
                'required': 'Devi assegnare la segnalazione ad almeno un utente.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Titolo"
        self.fields['title'].help_text = "Inserisci un titolo descrittivo per la segnalazione"
        self.fields['description'].label = "Descrizione"
        self.fields['description'].help_text = "Descrivi dettagliatamente il problema o la segnalazione"
        self.fields['category'].label = "Categoria"
        self.fields['category'].required = False
        self.fields['state'].label = "Stato"
        self.fields['priority'].label = "Priorità"
        self.fields['expired_date'].label = "Termine"
        self.fields['expired_date'].help_text = "Data entro cui risolvere la segnalazione"
        self.fields['expired_date'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d',
        )
        self.fields['expired_date'].input_formats = settings.DATE_INPUT_FORMATS

        assignee_choices = list(self.fields['assignee'].choices)
        cc_choices = list(assignee_choices)
        assignee_choices.append((1000, 'Tutti'))

        self.fields['assignee'] = forms.MultipleChoiceField(
            choices=assignee_choices,
            widget=forms.CheckboxSelectMultiple,
            label="Assegnatario",
            help_text="Seleziona uno o più utenti a cui assegnare la segnalazione",
            error_messages={
                'required': 'Devi selezionare almeno un assegnatario.',
            },
        )
        self.fields['cc'] = forms.MultipleChoiceField(
            choices=cc_choices,
            widget=forms.CheckboxSelectMultiple,
            label="Utenti in CC",
            help_text="Utenti che riceveranno notifiche senza essere assegnatari diretti",
            required=False,
        )

        # Pre-select current M2M values when editing an existing instance
        if self.instance and self.instance.pk:
            self.initial['assignee'] = [str(u.pk) for u in self.instance.assignee.all()]
            self.initial['cc'] = [str(u.pk) for u in self.instance.cc.all()]

    def clean(self):
        cleaned_data = super().clean()
        if 'assignee' in cleaned_data:
            user_ids = cleaned_data['assignee']
            if '1000' in user_ids:
                cleaned_data['assignee'] = User.objects.all()
            else:
                cleaned_data['assignee'] = [User.objects.get(id=i) for i in user_ids]
        if 'cc' in cleaned_data:
            user_cc_ids = cleaned_data['cc']
            cleaned_data['cc'] = [User.objects.get(id=i) for i in user_cc_ids]
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'Il mio commento',
        }
        error_messages = {
            'body': {
                'required': 'Il commento non può essere vuoto.',
            },
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Scrivi qui il tuo commento...',
            }),
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('file', 'description')
        labels = {
            'file': 'File',
            'description': 'Descrizione',
        }

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f and f.size > 10 * 1024 * 1024:
            raise ValidationError('Il file non può superare i 10 MB.')
        return f
