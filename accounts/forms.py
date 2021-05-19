from django import forms
from .models import Patient, Admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField

class PatientForm(forms.ModelForm):
    first_name = forms.CharField(help_text="Please enter your first name.")
    last_name = forms.CharField(help_text="Please enter your last name.")
    email = forms.CharField(help_text="Please enter your email address.")
    password1 = forms.CharField(help_text="Please enter a password.")
    password2 = forms.CharField(help_text="Please confirm your password.")
    
    class Meta: 
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class AdminForm(forms.ModelForm):
    first_name = forms.CharField(help_text="Please enter your first name.")
    last_name = forms.CharField(help_text="Please enter your last name.")
    email = forms.CharField(help_text="Please enter your email address.")
    password1 = forms.CharField(help_text="Please enter a password.")
    password2 = forms.CharField(help_text="Please confirm your password.")
    
    class Meta: 
        model = Admin
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']