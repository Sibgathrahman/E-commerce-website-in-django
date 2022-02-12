from django import forms
from django.contrib.auth import models
from django.forms import fields
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password','username']

        
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("password does not match!")

    def __init__(self, *args, **kwars):
        super(RegistrationForm, self).__init__(*args, **kwars)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

