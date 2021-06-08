from django.contrib.auth.forms import AuthenticationForm
from django.http.response import JsonResponse
from .forms import PatientForm, PatientSignupForm, DoctorSignupForm, AdminSignupForm
from .models import Patient
from . import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'Thesis/index.html')

#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'Thesis/adminclick.html')

#for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'Thesis/doctorclick.html')

#for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'Thesis/patientclick.html')

def admin_signup_view(request):
    admin_form=AdminSignupForm()
    if request.method=='POST':
        admin_form=AdminSignupForm(request.POST)
        if admin_form.is_valid():
            user=admin_form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('/adminlogin')
    return render(request,'Thesis/adminsignup.html',{'admin_form':admin_form})

def doctor_signup_view(request):
    user_form=forms.DoctorSignupForm()
    doctor_form=forms.DoctorForm()
    if request.method=='POST':
        user_form=forms.DoctorSignupForm(request.POST)
        doctor_form=forms.DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            doctor=doctor_form.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('/doctorlogin')
    return render(request,'Thesis/doctorsignup.html',{'user_form':user_form, 'doctor_form':doctor_form})

def patient_signup_view(request):
    patient_form=forms.PatientSignupForm()
    if request.method=='POST':
        patient_form=forms.PatientSignupForm(request.POST)
        if patient_form.is_valid():
            user=patient_form.save()
            user.set_password(user.password)
            user.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            return HttpResponseRedirect('/patientlogin')
    return render(request,'Thesis/patientsignup.html',{'patient_form': patient_form})

#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        return redirect('doctor-dashboard') 
    elif is_patient(request.user):
        return redirect('patient-dashboard')

@login_required(login_url='/adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    return render(request,'Thesis/admin-dashboard.html')

@login_required(login_url='/doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    return render(request,'Thesis/doctor-dashboard.html')

@login_required(login_url='/patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    return render(request,'Thesis/patient-dashboard.html')

@csrf_exempt
def patient_profile(request):
    data = {}
    if request.method == "GET":
        patient_id = request.GET.get("patient_id") 
        post = get_object_or_404(Patient, pk=patient_id)
        form = PatientForm(instance=post)
        context = {"form": form, "id": patient_id}
        data["html_form"] = render_to_string(
            "Thesis/patient_profile.html", context, request=request
        )

    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        instance = get_object_or_404(Patient, id=patient_id)
        form = PatientForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
        
        else:
            data["form_is_valid"] = False
        context = {"form": form}
    data["html_form"] = render_to_string(
        "Thesis/patient_profile.html", context, request=request
    )

    return JsonResponse(data)