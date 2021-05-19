from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=254, null=True)
    password1 = models.CharField(max_length=128, null=True)
    password2 = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return self.last_name

class Admin(models.Model):
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=254, null=True)
    password1 = models.CharField(max_length=128, null=True)
    password2 = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return self.last_name