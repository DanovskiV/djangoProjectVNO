from django.db import models
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'type': 'password',
                                                             'class': 'form-group first col-sm-3 form-control',
                                                             'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'type': 'password',
                                                             'class': 'form-group first col-sm-3 form-control',
                                                             'placeholder': 'Повторите пароль'}))

    username = forms.CharField(label="", widget=forms.TextInput(attrs={'type': 'text',
                                                             'class': 'form-group first col-sm-3 form-control',
                                                             'placeholder': 'Введите никнейм'}))

    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'type': 'text',
                                                             'class': 'form-group first col-sm-3 form-control',
                                                             'placeholder': 'Введите имя'}))

    email = forms.CharField(label="", widget=forms.TextInput(attrs={'type': 'text',
                                                             'class': 'form-group first col-sm-3 form-control',
                                                             'placeholder': 'Введите почтовый адрес'}))
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
                                                             'placeholder': 'Введите никнейм'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'type': 'password',
                                                             'class': 'form-group last col-sm-3 form-control',
                                                             'placeholder': 'Введите пароль'}))