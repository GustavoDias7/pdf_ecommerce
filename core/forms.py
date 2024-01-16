from django import forms
from .models import User
from utils.validators import validate_credit_card, is_expired, is_cpf


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class CreditCardForm(forms.Form):
    card_number = forms.CharField(max_length=25, validators=[validate_credit_card])
    card_name = forms.CharField(min_length=3, max_length=50)
    expiry = forms.DateField(validators=[is_expired])
    cvv = forms.IntegerField(max_value=9999)
    installments = forms.IntegerField(max_value=99)


class BoletoForm(forms.Form):
    cpf = forms.CharField(validators=[is_cpf])
