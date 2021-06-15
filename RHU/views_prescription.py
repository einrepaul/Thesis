import logging
from datetime import datetime
from RHU import logger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from RHU.forms import PrescriptionForm
from RHU.models import Account, Prescription, Action
from RHU import views
from django.core.exceptions import ObjectDoesNotExist

console_logger = logging.getLogger(__name__)

def patient_list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR,Account.ACCOUNT_PATIENT])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        prescriptions = Prescription.objects.filter(doctor=request.user)
    else:
        prescriptions = Prescription.objects.all()
    template_data['query'] = prescriptions.order_by('date')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'doctor':
            template_data['query'] = prescriptions.order_by('doctor__username', 'date')
        elif request.GET['sort'] == 'patient':
            template_data['query'] = prescriptions.order_by('patient__username', 'date')
        elif request.GET['sort'] == 'cation':
            template_data['query'] = prescriptions.order_by('medication', 'date')
        elif request.GET['sort'] == 'strength':
            template_data['query'] = prescriptions.order_by('strength', 'date')
        elif request.GET['sort'] == 'refill':
            template_data['query'] = prescriptions.order_by('refill', 'date')
        elif  request.GET['sort'] == 'status':
            template_data['query'] = prescriptions.order_by('active', 'date', )
    return render(request, 'Thesis/prescription/patientlist.html', template_data)

def doctor_list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR,Account.ACCOUNT_PATIENT])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        prescriptions = Prescription.objects.filter(doctor=request.user)
    else:
        prescriptions = Prescription.objects.all()
    template_data['query'] = prescriptions.order_by('date')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'doctor':
            template_data['query'] = prescriptions.order_by('doctor__username', 'date')
        elif request.GET['sort'] == 'patient':
            template_data['query'] = prescriptions.order_by('patient__username', 'date')
        elif request.GET['sort'] == 'cation':
            template_data['query'] = prescriptions.order_by('medication', 'date')
        elif request.GET['sort'] == 'strength':
            template_data['query'] = prescriptions.order_by('strength', 'date')
        elif request.GET['sort'] == 'refill':
            template_data['query'] = prescriptions.order_by('refill', 'date')
        elif  request.GET['sort'] == 'status':
            template_data['query'] = prescriptions.order_by('active', 'date', )
    return render(request, 'Thesis/prescription/doctorlist.html', template_data)

def create_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Add Prescription"})
    default = {}
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        default['doctor'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = PrescriptionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            pres = Prescription(
                patient=form.cleaned_data['patient'].user,
                doctor=form.cleaned_data['doctor'].user,
                date=form.cleaned_data['date'],
                medication=form.cleaned_data['medication'],
                strength=form.cleaned_data['strength'],
                instruction=form.cleaned_data['instruction'],
                refill=form.cleaned_data['refill'],
            )
            pres.save()
            logger.log(Action.ACTION_PRESCRIPTION, 'Prescription Created', request.user)
            form = PrescriptionForm(default)  # Clean the form when the page is redisplayed
            form._errors = {}
            template_data['alert_success'] = "Successfully added your prescription!"
    else:
        form._errors = {}
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        form.disable_field('doctor')
        form.date = datetime.today()
    template_data['form'] = form
    return render(request, 'Thesis/prescription/create.html', template_data)