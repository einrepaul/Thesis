import logging

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from RHU.forms import MedicalInfoForm
from RHU.models import Action, Account, MedicalInfo
from RHU import logger
from RHU import views
from dal import autocomplete

console_logger = logging.getLogger(__name__)

def patient_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    default = {}
    template_data = views.parse_session(request, {'form_button': 'Save'})
    form = MedicalInfoForm(request.POST)
    template_data['form'] = form
    return render(request, 'Thesis/medicalinfo/patient.html', template_data)

def list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    medicalinfoes = MedicalInfo.objects.all()
    # Page sorting.
    template_data['query'] = medicalinfoes.order_by('patient')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'patient':
            template_data['query'] = medicalinfoes.order_by('patient')
        if request.GET['sort'] == 'bloodType':
            template_data['query'] = medicalinfoes.order_by('bloodType')
    return render(request, 'Thesis/medicalinfo/list.html', template_data)

def update_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Validation Check. Make sure an appointment exists for the given pk.
    pk = request.GET['pk']
    try:
        medicalinfo = MedicalInfo.objects.get(pk=pk)
    except Exception:
        request.session['alert_danger'] = "The requested medical info does not exist."
        return HttpResponseRedirect('/error/doctordenied/')
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Update Medical Info", 'form_action': "?pk=" + pk,
                                             'medicalinfo': medicalinfo})
    # Proceed with the rest of the view
    request.POST._mutable = True
    request.POST['patient'] = medicalinfo.patient.account.pk
    if request.method == 'POST':
        form = MedicalInfoForm(request.POST)
        if form.is_valid():
            form.assign(medicalinfo)
            medicalinfo.save()
            logger.log(Action.ACTION_MEDICALINFO, 'Medical info updated', request.user)
            template_data['alert_success'] = "The medical info has been updated!"
            template_data['form'] = form
    else:
        form = MedicalInfoForm(medicalinfo.get_populated_fields())
        form.disable_field('patient')
    template_data['form'] = form
    return render(request, 'Thesis/medicalinfo/update.html', template_data)    