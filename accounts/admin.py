from django.contrib import admin
from .models import Patient, Admin, Doctor

class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor,DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AdminList(admin.ModelAdmin):
    pass
admin.site.register(Admin, AdminList)

