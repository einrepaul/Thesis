from django.contrib import admin
from .models import Patient, Admin

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

class AdminList(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

admin.site.register(Patient, PatientAdmin)
admin.site.register(Admin, AdminList)

