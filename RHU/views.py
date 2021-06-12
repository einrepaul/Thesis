import logging
from django.http.response import HttpResponseServerError

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist

from RHU.forms import LoginForm, AccountRegisterForm
from RHU.models import Account, Profile, Action, MedicalInfo
from RHU import logger

from django.contrib.auth.decorators import login_required,user_passes_test

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'Thesis/index.html')

console_logger = logging.getLogger(__name__)

def authentication_check(request, required_roles=None, required_GET=None):
    if not request.user.is_authenticated:
        request.session['alert_danger'] = "You must be logged in to view that page."
        return HttpResponseRedirect('/')
    try:
        request.user.account
    except ObjectDoesNotExist:
        request.session['alert_danger'] = "Your account was not properly created, please try a different account."
        return HttpResponseRedirect('/logout')
    if required_roles and request.user.account.role not in required_roles:
        request.session['alert_danger'] = "You don't have permission to view that page."
        return HttpResponseRedirect('/error/denied')
    if required_GET:
        for key in required_GET:
            request.session['alert_danger'] = "Looks like you tried to use a malformed URL."
            return HttpResponseRedirect('/error/denied')

def parse_session(request, template_data=None):
    if template_data is None:
        template_data = {}
    if request.session.has_key('alert_successs'):
        template_data['alert_success'] = request.session.get('alert_success')
        del request.session['alert_success']
    if request.session.has_key('alert_danger'):
        template_data['alert_danger'] = request.session.get('alert_danger')
        del request.session['alert_danger']
    return template_data

def logout_view(request):
    if request.user.is_authenticated:
        logger.log(Action.ACTION_ACCOUNT, "Account logout", request.user)
    saved_data = {}
    if request.session.has_key('alert_success'):
        saved_data['alert_success'] = request.session['alert_success']
    else:
        saved_data['alert_success'] = "You have successfully logged out."
    if request.session.has_key('alert_danger'):
        saved_data['alert_danger'] = request.session['alert_danger']
    logout(request)
    if 'alert_success' in saved_data:
        request.session['alert_success'] = saved_data['alert_success']
    if 'alert_danger' in saved_data:
        request.session['alert_danger'] = saved_data['alert_danger']
    return HttpResponseRedirect('/')

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    template_data = parse_session(request, {'form_button': "Login"})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'].lower(),
                password=form.cleaned_data['password']
            )
            login(request, user)
            logger.log(Action.ACTION_ACCOUNT, "Account login", request.user)
            request.session['alert_success'] = 'Successfully logged in.'
            return HttpResponseRedirect('/profile')
    else:
        form = LoginForm()
    template_data['form'] = form
    return render(request, 'Thesis/adminlogin.html', template_data)

def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile')
    template_data = parse_session(request, {'form_button': 'Register'})
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['email'].lower(),
                form.cleaned_data['email'],
                form.cleaned_data['password_first']
            )
            profile = Profile(
                firstname=form.cleaned_data['firstname'],
                lastname=form.cleaned_data['lastname'],
            )
            profile.save()
            account = Account(role=Account.ACCOUNT_PATIENT, profile=profile, user=user)
            account.save()
            medicalinfo = MedicalInfo(patient=account.user, alzheimer=False, asthma=False,
                                      diabetes=False, stroke=False)
            medicalinfo.save()
            user = authenticate(
                username = form.cleaned_data['email'].lower(),\
                password=form.cleaned_data['password_first']
            )
            logger.log(Action.ACTION_ACCOUNT, "Account registered", user)
            logger.log(Action.ACTION_ACCOUNT, "Account login", user)
            login(request,user)
            request.session['alert_success'] = "Successfully registered."
            return HttpResponseRedirect('/profile')
    else:
        form = AccountRegisterForm()
    template_data['form'] = form
    return render(request, 'Thesis/adminsignup.html', template_data)

def error_denied_view(request):
    authentication_result = authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = parse_session(request)
    return render(request, 'Thesis/error/denied.html', template_data)


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

