from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from core.models import LinkModel


class LoginForm(ModelForm):

    class Meta:

        model = User

        fields = ('email', 'password')

        labels = {
            'email': 'E-Mail:',
            'password': 'Senha:',
        }

        widgets = {

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu e-mail institucional'
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua senha'
            }),

        }

        error_messages = {

            'email': {
                'required': 'Informe o e-mail.',
            },

            'password': {
                'required': 'Informe a senha.',
            }

        }


    def clean_email(self):

        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError(
                'Informe o e-mail.'
            )

        if not email.endswith('@cps.sp.gov.br'):
            raise ValidationError(
                'Informe seu e-mail institucional.'
            )

        return email


    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:

            try:

                user = User.objects.get(email=email)

            except User.DoesNotExist:

                raise ValidationError(
                    "Usuário com esse e-mail não encontrado."
                )

            authenticated_user = authenticate(
                username=user.username,
                password=password
            )

            if authenticated_user is None:

                raise ValidationError(
                    "Senha incorreta para o e-mail informado."
                )

            self.user = authenticated_user

        return cleaned_data


class LinkForm(forms.ModelForm):

    class Meta:

        model = LinkModel

        fields = ['titulo', 'link', 'observacao']

        widgets = {

            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título'
            }),

            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o link'
            }),

            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite uma observação'
            }),

        }