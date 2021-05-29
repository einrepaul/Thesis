from django.contrib import admin
from .models import Patient, Admin

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AdminList(admin.ModelAdmin):
    pass
admin.site.register(Admin, AdminList)

