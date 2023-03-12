# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from apps.authentication.models import User
from django.forms import ModelForm
CHOICES = (
        ('myUser', 'Usuario'),
        ('myTech', 'Tecnico'),
     
    )
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    CHOICES = (
        ('myUser', 'Usuario'),
        ('myTech', 'Tecnico'),
     
    )
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))
    
    myRole= forms.ChoiceField(
        required=True,
        label=('Assign reviewer'),choices=CHOICES,
      widget=forms.Select(  attrs={
                            "placeholder": "Password check",
                "class": "form-control"
        })
        
   )
    

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','myRole')
class ProfileSettings(forms.ModelForm):
    
        

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))
    location = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "location",
                "class": "form-control"
            }
        ))
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "City",
                "class": "form-control"
            }
        ))
    country = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Country",
                "class": "form-control"
            }
        ))
    postal_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Postal code",
                "class": "form-control"
            }
        ))
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "phone_number",
                "class": "form-control"
            }
        ))

    bio = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Biography",
                "class": "form-control",
                "style":"color:black"
            }
        ))
    profile_pic = forms.ImageField()
    class Meta:
        model = User
        fields = ( 'email','first_name','last_name','location','city','country','postal_code','bio','profile_pic','phone_number')
    
    
