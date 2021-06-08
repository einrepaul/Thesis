from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField

class PatientSignupForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class PatientForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['profile_pic', 'address', 'age', 'gender', 'mobile']

class DoctorSignupForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['mobile']


class AdminSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        