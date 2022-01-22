import logging

from django.shortcuts import render, redirect, reverse
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
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT, Account.ACCOUNT_DOCTOR, Account.ACCOUNT_ADMIN])
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
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT, Account.ACCOUNT_DOCTOR, Account.ACCOUNT_ADMIN])
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

def admin_list_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT, Account.ACCOUNT_DOCTOR, Account.ACCOUNT_ADMIN])
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
    return render(request, 'Thesis/appointment/adminlist.html', template_data)

def patient_update_view(request, pk):
    # Authentication check.
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    # Validation Check. Make sure an appointment exists for the given pk.

    try:
        appointment = Appointment.objects.get(id=pk)
    except Exception:
        request.session['alert_danger'] = "The requested appointment does not exist."
        return HttpResponseRedirect('/error/denied/')
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Update Appointment", 'form_action':"<int:pk>" + id,
                                             'appointment': appointment})
    # Proceed with the rest of the view
    request.POST._mutable = True
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        request.POST['patient'] = request.user.account.pk
    elif request.user.account.role == Account.ACCOUNT_DOCTOR:
        request.POST['doctor'] = request.user.account.pk
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.assign(appointment)
            appointment.save()
            logger.log(Action.ACTION_APPOINTMENT, 'Appointment updated', request.user)
            template_data['alert_success'] = "The appointment has been updated!"
            template_data['form'] = form
    else:
        form = AppointmentForm(appointment.get_populated_fields())
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        form.disable_field('patient')
    elif request.user.account.role == Account.ACCOUNT_DOCTOR:
        form.disable_field('doctor')
    template_data['form'] = form
    return render(request, 'Thesis/appointment/patientupdate.html', template_data)

    
def admin_approve_appointment(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT, Account.ACCOUNT_DOCTOR, Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        appointments = Appointment.objects.filter(patient=request.user)
    else:
        appointments = Appointment.objects.all().filter(active=False)
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
    return render(request, 'Thesis/appointment/adminapproval.html', template_data)

def approve_appointment_view(request, pk):
    appointment= Appointment.objects.get(id=pk)
    appointment.active=True
    appointment.save()
    return redirect(reverse('RHU:admin-appointment-approve'))

def reject_appointment_view(request,pk):
    appointment= Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('RHU:admin-appointment-approve')