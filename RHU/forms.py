from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import date
from dal import autocomplete
from django.forms import ModelForm

from RHU.models import Account, Profile, MedicalInfo, Appointment, MorbidityReport

def validate_username_available(username):
    if User.objects.filter(username=username).count():
        raise forms.ValidationError("That email is already registered") 

def validate_username_exists(username):
    if not User.objects.filter(username=username).count():
        raise forms.ValidationError("That email does not exist")

def validate_birthday(birthday):
    if birthday.year < (date.today().year - 200):
        raise forms.ValidationError("Please choose a later date")
    elif birthday > date.today():
        raise forms.ValidationError("Please choose an earlier date")

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

class PasswordForm(BasicForm):
    password_current = forms.CharField(label='Current Password', max_length=50, widget=forms.PasswordInput())
    setup_field(password_current, 'Enter your current password here')
    password_first = forms.CharField(label="New Password", max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter new password here")
    password_second = forms.CharField(label='', max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter new password again")

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password_current = cleaned_data.get('password_current')
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second:
            if password_first != password_second:
                self.mark_error('password_second', 'Passwords do not match')
            if password_current and password_current == password_first:
                self.mark_error('password_current', 'Your current and new passwords must be different')
        return cleaned_data

class ProfileForm(BasicForm):
    firstname = forms.CharField(label='First Name',max_length=50)
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(label='Last Name',max_length=50)
    setup_field(lastname, 'Enter last name here')
    sex = forms.ChoiceField(required=False, choices=Profile.GENDER)
    setup_field(sex)
    birthday = forms.DateField(required=False, validators=[validate_birthday])
    setup_field(birthday, 'Enter birthday as YYYY-MM-DD')
    phone = forms.CharField(required=False, max_length=20)
    setup_field(phone, 'Enter phone number here')

    def assign(self, profile):
        profile.firstname = self.cleaned_data['firstname']
        profile.lastname = self.cleaned_data['lastname']
        profile.sex = self.cleaned_data['sex']
        if self.cleaned_data['birthday'] is not None:
            profile.birthday = self.cleaned_data['birthday']
        profile.phone = self.cleaned_data['phone']

class MessageForm(BasicForm):
    target = forms.ModelChoiceField(queryset=Account.objects.all())
    setup_field(target)
    header = forms.CharField(max_length=300)
    setup_field(header, "Message header")
    body = forms.CharField(max_length=1000)
    setup_field(body, "Message body")

class MedicalInfoForm(BasicForm):
    date = forms.DateField()
    setup_field(date)
    caseNumber = forms.CharField(max_length=10) 
    setup_field(caseNumber)
    patient = forms.ModelChoiceField(queryset=Account.objects.filter(role=10))
    setup_field(patient)
    age = forms.CharField(max_length=3)
    setup_field(age)
    sex = forms.ChoiceField(required=False, choices=MedicalInfo.GENDER)
    setup_field(sex)
    civilStatus = forms.ChoiceField(required=False, choices=MedicalInfo.CIVIL_STATUS)
    setup_field(civilStatus)
    barangay = forms.ChoiceField(required=False, choices=MedicalInfo.BARANGAY)
    setup_field(barangay)
    temperature = forms.CharField(max_length=5)
    setup_field(temperature)
    pulse = forms.CharField(max_length=5)
    setup_field(pulse)
    respiration = forms.CharField(max_length=5)
    setup_field(respiration)
    bloodPressure = forms.CharField(max_length=10)
    setup_field(bloodPressure)
    bloodType = forms.ChoiceField(choices=MedicalInfo.BLOOD, required = False)
    setup_field(bloodType)
    height = forms.CharField(max_length=5)
    setup_field(height, 'height in cm')
    weight = forms.CharField(max_length=5)
    setup_field(weight, 'weight in kg')
    comments = forms.CharField(max_length=500, required=False)
    setup_field(comments, 'Enter additional information here')
    
    def assign(self, medicalInfo):
        medicalInfo.date = self.cleaned_data['date']
        medicalInfo.caseNumber = self.cleaned_data['caseNumber']
        medicalInfo.patient = self.cleaned_data['patient'].user
        medicalInfo.age = self.cleaned_data['age']
        medicalInfo.sex = self.cleaned_data['sex']
        medicalInfo.civilStatus = self.cleaned_data['civilStatus']
        medicalInfo.barangay = self.cleaned_data['barangay']
        medicalInfo.temperature = self.cleaned_data['temperature']
        medicalInfo.pulse = self.cleaned_data['pulse']
        medicalInfo.respiration = self.cleaned_data['respiration']
        medicalInfo.bloodPressure = self.cleaned_data['bloodPressure']
        medicalInfo.height = self.cleaned_data['height']
        medicalInfo.weight = self.cleaned_data['weight']
        medicalInfo.bloodType = self.cleaned_data['bloodType']
        medicalInfo.comments = self.cleaned_data['comments']

class AppointmentForm(BasicForm):
    description = forms.CharField(required=True, max_length=50)
    setup_field(description, 'Enter description here')
    doctor = forms.ModelChoiceField(queryset=Account.objects.filter(role=20))
    setup_field(doctor)
    patient = forms.ModelChoiceField(queryset=Account.objects.filter(role=10))
    setup_field(patient)
    startTime = forms.TimeField(label='Start Time')
    setup_field(startTime)
    endTime = forms.TimeField(label='End Time')
    setup_field(endTime)
    date = forms.DateField()
    setup_field(date)

    def assign(self, appointment):
        appointment.description = self.cleaned_data['description']
        appointment.doctor = self.cleaned_data['doctor'].user
        appointment.patient = self.cleaned_data['patient'].user
        appointment.startTime = self.cleaned_data['startTime']
        appointment.endTime = self.cleaned_data['endTime']
        appointment.date = self.cleaned_data['date']

class MedTestForm(BasicForm):
    name = forms.CharField(max_length=50)
    setup_field(name)
    date = forms.DateField()
    setup_field(date)
    description = forms.CharField(max_length=200)
    setup_field(description, "Enter description here")
    doctor = forms.ModelChoiceField(queryset=Account.objects.filter(role=20))
    setup_field(doctor)
    patient = forms.ModelChoiceField(queryset=Account.objects.filter(role=10))
    setup_field(patient)
    private = forms.BooleanField(required=False)
    setup_field(private)
    completed = forms.BooleanField(required=False)
    setup_field(completed)

    def assign(self, medtest):

        medtest.name = self.cleaned_data['name']
        medtest.date = self.cleaned_data['date']
        medtest.description = self.cleaned_data['description']
        medtest.doctor = self.cleaned_data['doctor']
        medtest.patient = self.cleaned_data['patient']
        medtest.private = self.cleaned_data['private']
        medtest.completed = self.cleaned_data['completed']

class PrescriptionForm(BasicForm):
    patient = forms.ModelChoiceField(queryset=Account.objects.filter(role=10))
    setup_field(patient)
    doctor = forms.ModelChoiceField(queryset=Account.objects.filter(role=20))
    setup_field(doctor)
    date = forms.DateField()
    setup_field(date)
    medication = forms.CharField(max_length=100)
    setup_field(medication, "Enter the medication here")
    strength = forms.CharField(max_length=30)
    setup_field(strength, "Enter the strength here")
    instruction = forms.CharField(max_length=200)
    setup_field(instruction, "Enter the instruction here")
    refill = forms.IntegerField()
    setup_field(refill, "Enter the number of refills")

class EmployeeRegisterForm(BasicForm):
    firstname = forms.CharField(max_length=50, label='First Name')
    setup_field(firstname, 'Enter first name here')
    lastname = forms.CharField(max_length=50, label='Last Name')
    setup_field(lastname, 'Enter a last name here')
    email = forms.EmailField(max_length=50, validators=[validate_username_available])
    setup_field(email, 'Enter email here')
    password_first = forms.CharField(label='Password', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_first, "Enter password here")
    password_second = forms.CharField(label='', min_length=1, max_length=50, widget=forms.PasswordInput())
    setup_field(password_second, "Enter password again")
    employee = forms.ChoiceField(required=False, choices=Account.EMPLOYEE_TYPES)
    setup_field(employee)

    def clean(self):
        cleaned_data = super(EmployeeRegisterForm, self).clean()
        password_first = cleaned_data.get('password_first')
        password_second = cleaned_data.get('password_second')
        if password_first and password_second and password_first != password_second:
            self.mark_error('password_second', 'Passwords do not match')
        return cleaned_data

class MorbidityReportForm(BasicForm):
    barangay = forms.ChoiceField(choices=MorbidityReport.BARANGAY)
    setup_field(barangay)
    disease = forms.CharField(max_length=100)
    setup_field(disease)
    classification = forms.ChoiceField(choices=MorbidityReport.CLASSIFICATION)
    setup_field(classification)
    cases = forms.IntegerField(label="No. of cases")
    setup_field(cases)

    def assign(self, report):
        report.barangay = self.cleaned_data['barangay']
        report.disease = self.cleaned_data['disease']
        report.classification = self.cleaned_data['classification']
        report.cases = self.cleaned_data['cases']
        