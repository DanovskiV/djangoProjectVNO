from django.db import models
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'type': 'text',
                                                             'class': 'form-group first col-sm-3 form-control',
                                                             'placeholder': 'Ваш email'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'type': 'password',
                                                             'class': 'form-group last col-sm-3 form-control',
                                                             'placeholder': 'Ваш пароль'}))