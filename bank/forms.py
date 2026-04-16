from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from bank.models import Bank, Branch


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BankCreationForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'swift_code', 'institution_number', 'description']


class BranchCreationForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_number', 'address', 'email', 'capacity']




