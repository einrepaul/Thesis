import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect

from RHU.forms import MedTestForm
from RHU.models import Account, Action, MedicalTest
from RHU import logger
from RHU import views

console_logger = logging.getLogger(__name__)

def patient_list_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        medtests = MedicalTest.objects.all()
    else: 
        medtests = MedicalTest.objects.filter(patient=request.user, private=False)
    template_data['query'] = medtests.order_by('date')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'doctor':
            template_data['query'] = medtests.order_by('doctor_username', 'date')
        if request.GET['sort'] == 'patient':
            template_data['query'] == medtests.order_by('patient_username', 'date')
        if request.GET['sort'] == 'description':
            template_data['query'] == medtests.order_by('description', 'date')
        if request.GET['sort'] == 'name':
            template_data['query'] == medtests.order_by('name', 'date')
    return render(request, 'Thesis/medtest/patientlist.html', template_data)

def doctor_list_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        medtests = MedicalTest.objects.all()
    else: 
        medtests = MedicalTest.objects.filter(patient=request.user, private=False)
    template_data['query'] = medtests.order_by('date')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'doctor':
            template_data['query'] = medtests.order_by('doctor_username', 'date')
        if request.GET['sort'] == 'patient':
            template_data['query'] == medtests.order_by('patient_username', 'date')
        if request.GET['sort'] == 'description':
            template_data['query'] == medtests.order_by('description', 'date')
        if request.GET['sort'] == 'name':
            template_data['query'] == medtests.order_by('name', 'date')
    return render(request, 'Thesis/medtest/doctorlist.html', template_data)

def create_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Upload"})
    # Proceed with the rest of the view
    default = {}
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        default['doctor'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = MedTestForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            medtest = MedicalTest(
                name=form.cleaned_data['name'],
                date=form.cleaned_data['date'],
                hospital=form.cleaned_data['hospital'],
                description=form.cleaned_data['description'],
                doctor=form.cleaned_data['doctor'].user,
                patient=form.cleaned_data['patient'].user,
                private=form.cleaned_data['private'],
                completed=form.cleaned_data['completed'],
            )
            medtest.save()
            logger.log(Action.ACTION_MEDTEST, 'Medical Test created', request.user)
            form = MedTestForm(default)  # Clean the form when the page is redisplayed
            form.disable_field('doctor')
            form._errors = {}
            template_data['alert_success'] = "Successfully uploaded the medical test!"
    else:
        form._errors = {}
    form.disable_field('doctor')
    # if request.user.account.role == Account.ACCOUNT_DOCTOR:
    # form.disable_field('performedBy')
    template_data['form'] = form
    return render(request, 'Thesis/medtest/upload.html', template_data)