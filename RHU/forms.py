from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import date

def validate_username_available(username):
    if User.objects.filter(username=username).count():
        raise forms.ValidationError("That email is already registered") 

def validate_username_exists(username):
    if not User.objects.filter(username=username).count():
        raise forms.ValidationError("That email does not exist")

def setup_field(field, placeholder=None):
    field.widget.attrs['class'] = 'form-control'
    if placeholder is not None:
        field.widget.attrs['placeholder'] = placeholder

class BasicForm(forms.Form): 
    def disable_field(self, field):
        self.fields[field].widget.attrs['disabled'] = ""

    def mark_error(self, field, description):
        """
        Marks the given field as errous. The given description is displayed when the form it generated
        :param field: The name of the field
        :param description: The error description
        """
        self._errors[field] = self.error_class([description])
        del self.cleaned_data[field]

class LoginForm(BasicForm):
    email = forms.EmailField(max_length=50, validators=[validate_username_exists])
    setup_field(email, 'Enter email here')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    setup_field(password, "Enter password here")

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.mark_error('password', 'Incorrect password')
        return cleaned_data

class AccountRegisterForm(BasicForm):
    firstname = forms.CharField(label='First Name', max_length=50)
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(label='Last Name', max_length=50)
    setup_field(lastname, 'Enter last name here')
    email = forms.EmailField(max_length=50, validators=[validate_username_available])
    setup_field(email, 'Enter email here')
    password_first = forms.CharField(label='Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, 'Enter password here')
    password_second = forms.CharField(label='Confirm Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, 'Enter password again')

    def clean(self):
        cleaned_data = super(AccountRegisterForm, self).clean()
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second and password_first != password_second:
            self.mark_error('password_second', 'Passwords do not match')
        return cleaned_data

        