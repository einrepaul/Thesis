from django import forms
from .models import Patient, Admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField

class PatientForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        


class AdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        