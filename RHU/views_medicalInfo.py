import logging

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from RHU.forms import MedicalInfoForm
from RHU.models import Action, Account, MedicalInfo
from RHU import logger
from RHU import views

console_logger = logging.getLogger(__name__)

def patient_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT])
    if authentication_result is not None: return authentication_result
    default = {}
    template_data = views.parse_session(request, {'form_button': 'Save'})
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        default['patient'] = request.user.account.pk
    else:
        request.session['alert_danger'] = 'The requested medical info does not exist.'
        return HttpResponseRedirect('/error/patientdenied')
    request.POST._mutable = True
    request.POST.update(default)
    form = MedicalInfoForm(request.POST)
    form.disable_field('patient')
    template_data['form'] = form
    return render(request, 'Thesis/medicalinfo/patient.html', template_data)

def list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': 'Save'})
    # Proceed with the rest of the view
    medicalinfoes = MedicalInfo.objects.all()
    # Page sorting.
    template_data['query'] = medicalinfoes.order_by('patient')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'patient':
            template_data['query'] = medicalinfoes.order_by('patient')
        if request.GET['sort'] == 'bloodType':
            template_data['query'] = medicalinfoes.order_by('bloodType')
        if request.GET['sort'] == 'allergy':
            template_data['query'] = medicalinfoes.order_by('allergy')
    return render(request, 'Thesis/medicalinfo/list.html', template_data)