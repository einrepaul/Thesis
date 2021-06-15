import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect

from RHU.forms import AppointmentForm
from RHU.models import Account, Appointment, Action
from RHU import logger
from RHU import views

console_logger = logging.getLogger(__name__)

def patient_create_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Create'})
    default = {}
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        default['patient'] = request.user.account.pk
    elif request.user.account.role == Account.ACCOUNT_DOCTOR:
        default['doctor'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = AppointmentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            appt = Appointment(
                doctor=form.cleaned_data['doctor'].user,
                patient=form.cleaned_data['patient'].user,
                description=form.cleaned_data['description'],
                startTime=form.cleaned_data['startTime'],
                endTime=form.cleaned_data['endTime'],
                date=form.cleaned_data['date'],
            )
            appt.save()
            logger.log(Action.ACTION_APPOINTMENT, 'Appointment created', request.user)
            form = AppointmentForm(default)
            form._errors = {}
            template_data['alert_success'] = 'Successfully created your appointment!'
    else:
        form._errors = {}
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        form.disable_field('patient')
    elif request.user.account.role == Account.ACCOUNT_DOCTOR:
        form.disable_field('doctor')
    template_data['form'] = form
    return render(request, 'Thesis/appointment/patientcreate.html', template_data)

def doctor_create_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Create'})
    default = {}
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        default['patient'] = request.user.account.pk
    elif request.user.account.role == Account.ACCOUNT_DOCTOR:
        default['doctor'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = AppointmentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            appt = Appointment(
                doctor=form.cleaned_data['doctor'].user,
                patient=form.cleaned_data['patient'].user,
                description=form.cleaned_data['description'],
                startTime=form.cleaned_data['startTime'],
                endTime=form.cleaned_data['endTime'],
                date=form.cleaned_data['date'],
            )
            appt.save()
            logger.log(Action.ACTION_APPOINTMENT, 'Appointment created', request.user)
            form = AppointmentForm(default)
            form._errors = {}
            template_data['alert_success'] = 'Successfully created your appointment!'
    else:
        form._errors = {}
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        form.disable_field('patient')
    elif request.user.account.role == Account.ACCOUNT_DOCTOR:
        form.disable_field('doctor')
    template_data['form'] = form
    return render(request, 'Thesis/appointment/doctorcreate.html', template_data)

def patient_list_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT, Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        appointments = Appointment.objects.filter(patient=request.user)
    else:
        appointments = Appointment.objects.all()
    template_data['query'] = appointments.order_by('date', 'startTime')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'doctor':
            template_data['query'] = appointments.order_by('doctor_username', 'date', 'startTime')
        if request.GET['sort'] == 'patient':
            template_data['query'] = appointments.order_by('patient_username', 'date', 'startTime')
        if request.GET['sort'] == 'description':
            template_data['query'] = appointments.order_by('description', 'date', 'startTime')
        if request.GET['sort'] == 'status':
            template_data['query'] = appointments.order_by('active', 'date', 'startTime')
    return render(request, 'Thesis/appointment/patientlist.html', template_data)

def doctor_list_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT, Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        appointments = Appointment.objects.filter(patient=request.user)
    else:
        appointments = Appointment.objects.all()
    template_data['query'] = appointments.order_by('date', 'startTime')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'doctor':
            template_data['query'] = appointments.order_by('doctor_username', 'date', 'startTime')
        if request.GET['sort'] == 'patient':
            template_data['query'] = appointments.order_by('patient_username', 'date', 'startTime')
        if request.GET['sort'] == 'description':
            template_data['query'] = appointments.order_by('description', 'date', 'startTime')
        if request.GET['sort'] == 'status':
            template_data['query'] = appointments.order_by('active', 'date', 'startTime')
    return render(request, 'Thesis/appointment/doctorlist.html', template_data)
    