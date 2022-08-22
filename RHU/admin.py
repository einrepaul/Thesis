from django.contrib import admin
from RHU.resources import MedicalInfoResource

from import_export import resources
import import_export
from import_export.admin import ImportExportModelAdmin

from RHU.models import Account, Profile, Action, Appointment, MedicalTest, Statistics, MorbidityReport, MedicalInfo
from RHU.models import Account, Profile, Action, Appointment, MedicalTest, Statistics, MorbidityReport, MedicalInfo
#from RHU.models import Account, Profile, Action, TimeSlot, Appointment, MedicalTest, Statistics, MorbidityReport, MedicalInfo

class AccountAdmin(admin.ModelAdmin):
    fields = ['role', 'profile', 'user']
    list_display = ('role', 'profile')

admin.site.register(Account, AccountAdmin)

class ProfileAdmin(admin.ModelAdmin):
    fields = [
        'firstname',
        'lastname',
        'sex',
        'birthday',
        'phone'
    ]

    list_display = ('firstname', 'lastname', 'birthday', 'created')

admin.site.register(Profile, ProfileAdmin)

class ActionAdmin(admin.ModelAdmin):
    readonly_fields = ('timePerformed',)
    fields = [
        'type',
        'description',
        'user',
    ]
    list_display = ['user', 'type', 'description', 'timePerformed']
    list_filter = ('user', 'type', 'timePerformed')
    ordering = ('-timePerformed',)

admin.site.register(Action, ActionAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    fields = [
        'doctor',
        'patient',
        'description',
        'active',
<<<<<<< HEAD
        'timeslot',
        'appt_date'
    ]
    list_display = ('description','doctor', 'patient', 'active', 'timeslot', 'appt_date')
=======
<<<<<<< HEAD
<<<<<<< HEAD
       # 'timeslot',
      #  'appt_date'
    ]
   # list_display = ('description','doctor', 'patient', 'active', 'timeslot', 'appt_date')
=======
        'startTime',
        'endTime',
        'date'
    ]
    list_display = ('description','doctor', 'patient', 'active', 'startTime', 'endTime', 'date')
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
=======
        'startTime',
        'endTime',
        'date'
    ]
    list_display = ('description','doctor', 'patient', 'active', 'startTime', 'endTime', 'date')
>>>>>>> 6bf3e3fe447291cfbadb205f2fb6e0f6a2d27e3a
>>>>>>> 66334453f42d854a7d5194ad003c97a94a6f8296

#admin.site.register(Appointment, AppointmentAdmin)

class TimeSlotAdmin(admin.ModelAdmin):
    fields = [
        'startTime',
        'endTime',
        'date'
       # 'end_date'
    ]
    list_display = ('description','date', 'doctor', 'patient', 'startTime', 'endTime', 'active')
    #list_display = ('startTime', 'endTime', 'end_date')

admin.site.register(Appointment, AppointmentAdmin)

#admin.site.register(TimeSlot, TimeSlotAdmin)

class MedicalInfoAdmin(admin.ModelAdmin):
    fields = [
        'caseNumber',
        'patient',
        'age',
        'sex',
        'civilStatus',
        'barangay',
        'temperature',
        'pulse',
        'respiration',
        'bloodPressure',
        'height',
        'weight',
        'bloodType',
        'comments',
    ]
   
class MedicalInfoAdmin(ImportExportModelAdmin):

    resource_class = MedicalInfoResource

    list_display = ('caseNumber', 'patient', 'age', 'sex', 
    'civilStatus', 'barangay', 'temperature', 'pulse', 'respiration', 
    'bloodPressure', 'bloodType', 'height', 'weight', 'comments')
    pass

admin.site.register(MedicalInfo, MedicalInfoAdmin)

class MedicalTestAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'date',
        'description',
        'doctor',
        'patient',
        'private',
        'completed'
    ]
    list_display = ('name', 'doctor', 'patient', 'date')
    
admin.site.register(MedicalTest, MedicalTestAdmin)

class MedicalTestResource(resources.ModelResource):

    class Meta:
        model = MedicalTest

class StatsAdmin(admin.ModelAdmin):
    readonly_fields = ('stats', 'freq')
    list_filter = ('stats','freq')

admin.site.register(Statistics, StatsAdmin)

class MorbidityAdmin(admin.ModelAdmin):
    fields = [
        'barangay',
        'disease',
        'classification',
        'cases',
    ]
    list_display = ('barangay', 'disease', 'classification', 'cases', 'latitude', 'longitude')
    readonly_fields = ('latitude', 'longitude')
    
admin.site.register(MorbidityReport, MorbidityAdmin)



