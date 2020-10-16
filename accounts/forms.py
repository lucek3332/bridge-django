from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        help_texts = {
            'username': ""
        }

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email'] == "":
            raise ValidationError("Proszę podać email.")
        return cd['email']


class ProfileRegisterForm(forms.Form):
    photo = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea, label="Opis", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Powtórz hasło")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("Hasła nie są identyczne!")
        return cd['password2']
