from django import forms
from django.core.exceptions import ValidationError
from gestione_comune import settings
from .models import Issue, Comment
from django.contrib.auth.models import User

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'description', 'assignee', 'cc', 'state', 'priority', 'expired_date')
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
        self.fields['state'].label = "Stato"
        self.fields['priority'].label = "Priorità"
        self.fields['expired_date'].label = "Termine"
        self.fields['expired_date'].help_text = "Data entro cui risolvere la segnalazione (formato: gg/mm/aaaa)"
        self.fields['expired_date'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['expired_date'].widget.attrs.update({'class': 'datepicker', 'placeholder': 'gg/mm/aaaa'})

        assignee = [i for i in self.fields['assignee'].choices]
        cc = assignee.copy()
        assignee.append((1000, 'Tutti'))
        self.fields['assignee'] = forms.MultipleChoiceField(
            choices=assignee,
            widget=forms.CheckboxSelectMultiple,
            label="Assegnatario",
            help_text="Seleziona uno o più utenti a cui assegnare la segnalazione",
            error_messages={
                'required': 'Devi selezionare almeno un assegnatario.',
            }
        )
        self.fields['cc'] = forms.MultipleChoiceField(
            choices=cc,
            widget=forms.CheckboxSelectMultiple,
            label="Utenti in CC",
            help_text="Utenti che riceveranno notifiche senza essere assegnatari diretti",
            required=False
        )

    def clean(self):
        cleaned_data = super().clean()
        user_id = [i for i in cleaned_data['assignee']]
        if 'cc' in cleaned_data:
            user_cc_id = [i for i in cleaned_data['cc']]
            cleaned_data['cc'] = [User.objects.get(id=i) for i in user_cc_id]
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
            'body': 'Il mio commento',
            'post': '',
            'name': '',
        }
        error_messages = {
            'body': {
                'required': 'Il commento non può essere vuoto.',
                'max_length': 'Il commento è troppo lungo.',
            },
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Scrivi qui il tuo commento...'
            }),
            'post': forms.HiddenInput(),
            'name': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].help_text = "Aggiungi un commento per fornire aggiornamenti o informazioni aggiuntive"
