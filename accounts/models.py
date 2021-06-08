from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address=models.CharField(max_length=40, null=True)
    mobile=models.CharField(max_length=20, null=True)
    age=models.IntegerField(null=True)
    gender=models.CharField(max_length=20, null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} {}".format(self.user.first_name,self.user.last_name)

class Doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    mobile=models.CharField(max_length=20, null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} {}".format(self.user.first_name,self.user.last_name)

class Admin(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id