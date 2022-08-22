from datetime import date
import datetime
import geocoder

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER = (
        ('', '-----'),
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
    sex = models.CharField(default=0, blank=True, max_length=1, choices=GENDER)
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
  #  ACTION_TIMESLOT = 4
 #   ACTION_APPOINTMENT = 5
  #  ACTION_MEDTEST = 6
  #  ACTION_PRESCRIPTION = 7
  #  ACTION_ADMISSION = 8
  #  ACTION_MEDICALINFO = 9
  #  ACTION_MESSAGE = 10
  #  ACTION_MORBIDITYREPORT = 11
    ACTION_TYPES = (
        (ACTION_NONE, "None"),
        (ACTION_ACCOUNT, "Account"),
        (ACTION_PATIENT, "Patient"),
        (ACTION_ADMIN, "Admin"),
       # (ACTION_TIMESLOT, "Time Slot"),
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
    GENDER = (
        ('', '-----'),
        ('M', 'Male'),
        ('F', 'Female'),
    )

    BARANGAY = (
        ('', '------'),
        ('Aripdip', 'Aripdip'),
        ('Ilongbukid', 'Ilongbukid'),
        ('Poscolon', 'Poscolon'),
        ('San Florentino', 'San Florentino'),
        ('Calaigang', 'Calaigang'),
        ('San Dionisio', 'San Dionisio'),
    )

    BLOOD = (
        ('', '-----'),
        ('A+', 'A+ TYPE'),
        ('B+', 'B+ TYPE'),
        ('AB+', 'AB+ TYPE'),
        ('O+', 'O+ TYPE'),
        ('A-', 'A- TYPE'),
        ('B-', 'B- TYPE'),
        ('AB-', 'AB- TYPE'),
        ('O-', 'O- TYPE'),
    )

    CIVIL_STATUS = (
        ('', '-----'),
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated'),
        ('Widowed', 'Widowed'),
    )

    class Meta:
        verbose_name_plural = 'Medical Info'

    @staticmethod
    def toBlood(key):
        for item in MedicalInfo.BLOOD:
            if item[0] == key:
                return item[1]
        return "None"

    @staticmethod
    def toGender(key):
        for item in MedicalInfo.GENDER:
            if item[0] == key:
                return item[1]
        return "None"

    @staticmethod
    def toCivilStatus(key):
        for item in MedicalInfo.CIVIL_STATUS:
            if item[0] == key:
                return item[1]
        return "None"

    caseNumber = models.CharField(max_length=10, primary_key=True, unique=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    age = models.CharField(max_length=3, null=True)
    sex = models.CharField(default=0, blank=True, max_length=1, choices=GENDER)
    civilStatus = models.CharField(default=0, blank=True, max_length=20, choices=CIVIL_STATUS)
    barangay = models.CharField(default=0, blank=True, max_length=50, choices=BARANGAY)
    temperature = models.CharField(max_length=5, null=True)
    pulse = models.CharField(max_length=5, null=True)
    respiration = models.CharField(max_length=5, null=True)
    bloodPressure = models.CharField(max_length=10, null=True)
    height = models.CharField(max_length=5, null=True)
    weight = models.CharField(max_length=5, null=True)
    bloodType = models.CharField(default=0, max_length=10, choices=BLOOD)
    comments = models.CharField(max_length=700)

    def get_populated_fields(self):
        fields = {
            'case_number': self.caseNumber,
            'patient': self.patient.user,
            'age': self.age,
            'sex': self.sex,
            'civil_status': self.civilStatus,
            'barangay': self.barangay,
            'temperature': self.temperature,
            'pulse': self.pulse,
            'respiration': self.respiration,
            'bloodPressure': self.bloodPressure,
            'height': self.height,
            'weight': self.weight,
            'bloodType': self.bloodType,
            'comments': self.comments,
        }
        return fields

class Message(models.Model):
    message_id = models.CharField(max_length=10, primary_key=True, unique=True)
    target = models.ForeignKey(Account, related_name='messages_received', on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, related_name='messages_sent', on_delete=models.CASCADE)
    header = models.CharField(max_length=300)
    body = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class TimeSlot(models.Model):
    timeslot_id = models.CharField(max_length=10, primary_key=True, unique=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    end_date = models.DateField(null=True)

    def __str__(self):
       return str(self.startTime) + "-" + str(self.endTime)

    def get_populated_fields(self):
        fields = {
            'startTime': self.startTime,
            'endTime': self.endTime,
            'end_date': self.end_date,
        }

    class Meta:
        verbose_name_plural = 'Time Slots'

class Appointment(models.Model):
<<<<<<< HEAD
    appointment_id = models.CharField(max_length=10, primary_key=True)
=======
<<<<<<< HEAD
<<<<<<< HEAD
    
=======
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
=======
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
>>>>>>> 66334453f42d854a7d5194ad003c97a94a6f8296
    doctor = models.ForeignKey(User, related_name='doctors', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patients', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
<<<<<<< HEAD
    timeslot = models.ForeignKey(TimeSlot, related_name='timeslots', on_delete=models.CASCADE)
    appt_date = models.ForeignKey(TimeSlot, null=True, related_name='slotdates', on_delete=models.CASCADE)
=======
    startTime = models.TimeField(null=True)
    endTime = models.TimeField(null=True)
    date = models.DateField(null=True)
<<<<<<< HEAD
<<<<<<< HEAD
   
=======
=======
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
>>>>>>> 66334453f42d854a7d5194ad003c97a94a6f8296

>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
    def get_populated_fields(self):
        fields = {
        
            'doctor': self.doctor.account,
            'patient': self.patient.account,
            'description': self.description,
<<<<<<< HEAD
            'timeslot': self.timeslot,
            'appt_date': self.appt_date.date,
=======
            'startTime': self.startTime,
            'endTime': self.endTime,
            'date': self.date,
<<<<<<< HEAD
<<<<<<< HEAD
            
            #'timeslot': self.timeslot,
            #'appt_date': self.appt_date.date,
=======
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
=======
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
>>>>>>> 66334453f42d854a7d5194ad003c97a94a6f8296
        }
        return fields

    class Meta:
        verbose_name_plural = 'Appointments'

class MedicalTest(models.Model):
    medtest_id = models.CharField(max_length=10, primary_key=True, unique=True)
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
    prescription_id = models.CharField(max_length=10, primary_key=True, unique=True)
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor', on_delete=models.CASCADE)
    date = models.DateField()
    medication = models.CharField(max_length=100)
    strength = models.CharField(max_length=30)
    instruction = models.CharField(max_length=200)
    refill = models.IntegerField()
    active = models.BooleanField(default=True)

class Statistics(models.Model):
    stats_id = models.CharField(max_length=10, primary_key=True, default="")
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
   
<<<<<<< HEAD
    report_id = models.CharField(max_length=10, primary_key=True, unique=True)
=======
<<<<<<< HEAD
<<<<<<< HEAD
    
=======
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
=======
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
>>>>>>> 66334453f42d854a7d5194ad003c97a94a6f8296
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

    

    