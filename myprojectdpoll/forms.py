from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={"class": "form-control"}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
