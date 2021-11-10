from datetime import date
import datetime
import geocoder

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    @staticmethod
    def toGender(key):
        for item in Profile.GENDER:
            if item[0] == key:
                return item[1]
        return "None"

    firstname = models.CharField(blank=True, max_length=50)
    lastname = models.CharField(blank=True, max_length=50)
    sex = models.CharField(blank=True, max_length=1, choices=GENDER)
    birthday = models.DateField(default=date(1000, 1, 1))
    phone = models.CharField(blank=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def get_populated_fields(self):
        fields = {}
        if self.firstname is not None:
            fields['firstname'] = self.firstname
        if self.lastname is not None:
            fields['lastname'] = self.lastname
        if self.sex is not None:
            fields['sex'] = self.sex
        if not self.birthday.year == 1000:
            fields['birthday'] = self.birthday
        if self.phone is not None:
            fields['phone'] = self.phone
        return fields
        
    def __str__(self):
        return self.firstname + " " + self.lastname

class Account(models.Model):
    ACCOUNT_UNKNOWN = 0
    ACCOUNT_PATIENT = 10
    ACCOUNT_DOCTOR = 20
    ACCOUNT_ADMIN = 30
    ACCOUNT_TYPES = (
        (ACCOUNT_UNKNOWN, "Unknown"),
        (ACCOUNT_PATIENT, "Patient"),
        (ACCOUNT_DOCTOR, "Doctor"),
        (ACCOUNT_ADMIN, "Admin"),
    )
    EMPLOYEE_TYPES = (
        (ACCOUNT_DOCTOR, "Doctor"),
        (ACCOUNT_ADMIN, "Admin"),
    )

    @staticmethod
    def toAccount(key):
        for item in Account.ACCOUNT_TYPES:
            if item[0] == key:
                return item[1]
        return "None"

    role = models.IntegerField(default = 0, choices = ACCOUNT_TYPES)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.role == 30:
            return "Nurse. " + self.profile.__str__()
        elif self.role == 20:
            return "Dr. " + self.profile.__str__()
        else:
            return self.profile.__str__()
    
    class Admin:
        list_display = (
            'role',
            'profile',
            'user'
        )

class Action(models.Model):
    ACTION_NONE = 0
    ACTION_ACCOUNT = 1
    ACTION_PATIENT = 2
    ACTION_ADMIN = 3
    ACTION_APPOINTMENT = 4
    ACTION_MEDTEST = 5
    ACTION_PRESCRIPTION = 6
    ACTION_ADMISSION = 7
    ACTION_MEDICALINFO = 8
    ACTION_MESSAGE = 9
    ACTION_MORBIDITYREPORT = 10
    ACTION_TYPES = (
        (ACTION_NONE, "None"),
        (ACTION_ACCOUNT, "Account"),
        (ACTION_PATIENT, "Patient"),
        (ACTION_ADMIN, "Admin"),
        (ACTION_APPOINTMENT, "Appointment"),
        (ACTION_MEDTEST, "Medical Test"),
        (ACTION_PRESCRIPTION, "Prescription"),
        (ACTION_ADMISSION, "Admission"),
        (ACTION_MEDICALINFO, "Medical Info"),
        (ACTION_MESSAGE, "Message"),
        (ACTION_MORBIDITYREPORT, "Morbidity Report"),
    )

    @staticmethod
    def toAction(key):
        for item in Action.ACTION_TYPES:
            if item[0] == key:
                return item[1]
        return "None"

    type = models.IntegerField(default=0, choices=ACTION_TYPES)
    timePerformed = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class MedicalInfo(models.Model):
    BLOOD = (
        ('A+', 'A+ TYPE'),
        ('B+', 'B+ TYPE'),
        ('AB+', 'AB+ TYPE'),
        ('O+', 'O+ TYPE'),
        ('A-', 'A- TYPE'),
        ('B-', 'B- TYPE'),
        ('AB-', 'AB- TYPE'),
        ('O-', 'O- TYPE'),
    )
    class Meta:
        verbose_name_plural = 'Medical Info'

    @staticmethod
    def toBlood(key):
        for item in MedicalInfo.BLOOD:
            if item[0] == key:
                return item[1]
        return "None"

    patient = models.ForeignKey(User, related_name="patiento", on_delete=models.CASCADE)
    bloodType = models.CharField(max_length=10, choices=BLOOD)
    allergy = models.CharField(max_length=100)
    alzheimer = models.BooleanField()
    asthma = models.BooleanField()
    diabetes = models.BooleanField()
    stroke = models.BooleanField()
    comments = models.CharField(max_length=700)

    def get_populated_fields(self):
        fields = {
            'patient': self.patient.account,
            'bloodType': self.bloodType,
            'allergy': self.allergy,
            'alzheimer': self.alzheimer,
            'asthma': self.asthma,
            'diabetes': self.diabetes,
            'stroke': self.stroke,
            'comments': self.comments,
        }
        return fields

class Message(models.Model):
    target = models.ForeignKey(Account, related_name='messages_received', on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, related_name='messages_sent', on_delete=models.CASCADE)
    header = models.CharField(max_length=300)
    body = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    doctor = models.ForeignKey(User, related_name='doctors', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patients', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    date = models.DateField()

    def get_populated_fields(self):
        fields = {
            'doctor': self.doctor.account,
            'patient': self.patient.account,
            'description': self.description,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'date': self.date,
        }
        return fields

class MedicalTest(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField()
    description = models.CharField(max_length=200)
    doctor = models.ForeignKey(User, related_name='docs', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='pts', on_delete=models.CASCADE)
    private = models.BooleanField(default=True)
    completed = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Medical Tests'

    def get_populated_fields(self):

        fields = {
            'name': self.name,
            'date': self.date,
            'description': self.description,
            'doctor': self.doctor.account,
            'patient': self.patient.account,
            'private': self.private,
            'completed': self.completed,
        }

        return fields

class Prescription(models.Model):
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    date = models.DateField()
    medication = models.CharField(max_length=100)
    strength = models.CharField(max_length=30)
    instruction = models.CharField(max_length=200)
    refill = models.IntegerField()
    active = models.BooleanField(default=True)

class Statistics(models.Model):
    stats = models.CharField(max_length=100)
    freq = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Statistics'

class MorbidityReport(models.Model):
    BARANGAY = (
        ('Aripdip', 'Aripdip'),
        ('Ilongbukid', 'Ilongbukid'),
        ('Poscolon', 'Poscolon'),
        ('San Florentino', 'San Florentino'),
        ('Calaigang', 'Calaigang'),
        ('San Dionisio', 'San Dionisio'),
    )

    CLASSIFICATION = (
        ('C', 'Communicable Disease'),
        ('NC', 'Non-communicable Disease'),
    )

    @staticmethod
    def toBarangay(key):
        for item in MorbidityReport.BARANGAY:
            if item[0] == key:
                return item[1]
        return "None"

    @staticmethod
    def toClassification(key):
        for item in MorbidityReport.CLASSIFICATION:
            if item[0] == key:
                return item[1]
        return "None"
 
    barangay = models.CharField(blank=True, max_length=50, choices=BARANGAY)
    disease = models.CharField(blank=True, max_length=100)
    classification = models.CharField(blank=True, max_length=10, choices=CLASSIFICATION)
    cases = models.IntegerField(blank=True, null=True)
    totalcases = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Morbidity Report'

    def get_populated_fields(self):

        fields = {
            'barangay': self.barangay,
            'disease':self.disease,
            'classification': self.classification,
            'cases': self.cases,
        }

        return fields

    def save(self, *args, **kwargs):
        self.latitude = geocoder.osm(self.barangay).lat
        self.longitude = geocoder.osm(self.barangay).lng
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.barangay

    

    