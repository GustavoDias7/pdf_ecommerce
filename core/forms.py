from django import forms
from .models import User


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class ContactForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=100)
    email = forms.EmailField(max_length=255)
    subject = forms.CharField(min_length=3, max_length=150)
    message = forms.CharField(min_length=3, max_length=400)

