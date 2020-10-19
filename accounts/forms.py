from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordResetForm
from accounts.tasks import send_mail_task
from django.template import loader


class UserRegisterForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        help_texts = {
            'username': ""
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Istnieje już konto z podanym mailem.")
        return email


class ProfileRegisterForm(forms.Form):
    photo = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Wpisz używane systemy licytacyjne"}), label="Opis", required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Powtórz hasło")

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cd = super().clean()
        password = cd.get("password")
        password2 = cd.get("password2")

        if password and password2:
            if password != password2:
                self.add_error("password2", "Hasła nie są identyczne!")


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        send_mail_task.delay(subject, body, from_email, [to_email])
