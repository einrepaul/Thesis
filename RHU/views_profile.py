import logging

from django.shortcuts import render
from django.contrib.auth import authenticate

from RHU import views
from RHU import logger
from RHU.models import Action
from RHU.forms import PasswordForm, ProfileForm

console_logger = logging.getLogger(__name__) 

def patient_profile_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    return render(request, 'Thesis/patient_profile.html', template_data)

def admin_profile_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    return render(request, 'Thesis/admin_profile.html', template_data)

def doctor_profile_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    return render(request, 'Thesis/doctor_profile.html', template_data)

def patient_password_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Change password'})
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password_current'])
            if user is None:
                form.mark_error('password_current', 'Incorrect password')
            else: 
                user = request.user
                user.set_password(form.cleaned_data['password_first'])
                user.save()
                logger.log(Action.ACTION_ACCOUNT, "Account password change", request.user)
                form = PasswordForm()
                template_data['alert_success'] = 'Your password has been changed!'
    else:
        form = PasswordForm()
    template_data['form'] = form
    return render(request, 'Thesis/profile/patient_password.html', template_data)

def doctor_password_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Change password'})
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password_current'])
            if user is None:
                form.mark_error('password_current', 'Incorrect password')
            else: 
                user = request.user
                user.set_password(form.cleaned_data['password_first'])
                user.save()
                logger.log(Action.ACTION_ACCOUNT, "Account password change", request.user)
                form = PasswordForm()
                template_data['alert_success'] = 'Your password has been changed!'
    else:
        form = PasswordForm()
    template_data['form'] = form
    return render(request, 'Thesis/profile/doctor_password.html', template_data)

def admin_password_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Change password'})
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password_current'])
            if user is None:
                form.mark_error('password_current', 'Incorrect password')
            else: 
                user = request.user
                user.set_password(form.cleaned_data['password_first'])
                user.save()
                logger.log(Action.ACTION_ACCOUNT, "Account password change", request.user)
                form = PasswordForm()
                template_data['alert_success'] = 'Your password has been changed!'
    else:
        form = PasswordForm()
    template_data['form'] = form
    return render(request, 'Thesis/profile/admin_password.html', template_data)

def patient_update_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Update Profile'})
    profile = request.user.account.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.assign(profile)
            profile.save()
            logger.log(Action.ACTION_ACCOUNT, "Account updated", request.user)
            template_data['alert_success'] = "Your profile has been updated!"
    else:
        form = ProfileForm(profile.get_populated_fields())
    template_data['form'] = form
    return render(request, 'Thesis/profile/patient_update.html', template_data)

def doctor_update_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Update Profile'})
    profile = request.user.account.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.assign(profile)
            profile.save()
            logger.log(Action.ACTION_ACCOUNT, "Account updated", request.user)
            template_data['alert_success'] = "Your profile has been updated!"
    else:
        form = ProfileForm(profile.get_populated_fields())
    template_data['form'] = form
    return render(request, 'Thesis/profile/doctor_update.html', template_data)

def admin_update_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Update Profile'})
    profile = request.user.account.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.assign(profile)
            profile.save()
            logger.log(Action.ACTION_ACCOUNT, "Account updated", request.user)
            template_data['alert_success'] = "Your profile has been updated!"
    else:
        form = ProfileForm(profile.get_populated_fields())
    template_data['form'] = form
    return render(request, 'Thesis/profile/admin_update.html', template_data)