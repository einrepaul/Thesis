from django.contrib import admin

from RHU.models import Account, Profile, Action, Appointment, MedicalTest, Statistics, MorbidityReport

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
        'startTime',
        'endTime',
        'date'
    ]
    list_display = ('description','date', 'doctor', 'patient', 'startTime', 'endTime', 'active')


admin.site.register(Appointment, AppointmentAdmin)

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

