from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.decorators import verified_email_required

@verified_email_required
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Your email address is not registered.")
        return email, render(
            "cradle/account/password_reset.html",
        )