import logging

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from RHU.forms import MedicalInfoForm
from RHU.models import Action, Account, MedicalInfo
from RHU import logger
from RHU import views
from RHU.utils import set_pagination

console_logger = logging.getLogger(__name__)

def patient_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    default = {}
    template_data = views.parse_session(request, {'form_button': 'Save'})
    form = MedicalInfoForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            medrecord = MedicalInfo(
                date=form.cleaned_data['date'],
                caseNumber=form.cleaned_data['caseNumber'],
                patient=form.cleaned_data['patient'].user,
                age=form.cleaned_data['age'],
                sex=form.cleaned_data['sex'],
                civilStatus=form.cleaned_data['civilStatus'],
                address=form.cleaned_data['address'],
                temperature=form.cleaned_data['temperature'],
                pulse=form.cleaned_data['pulse'],
                respiration=form.cleaned_data['respiration'],
                bloodPressure=form.cleaned_data['bloodPressure'],
                bloodType=form.cleaned_data['bloodType'],
                height=form.cleaned_data['height'],
                weight=form.cleaned_data['weight'],
                comments=form.cleaned_data['comments'],
            )
            medrecord.save()
            logger.log(Action.ACTION_MEDICALINFO, 'Medical Record created!', request.user)
            form = MedicalInfoForm(default)  # Clean the form when the page is redisplayed
            form._errors = {}
            template_data['alert_success'] = "Successfully created the medical record!"
    else:
        form._errors = {}
    template_data['form'] = form
    return render(request, 'Thesis/medicalinfo/patient.html', template_data)

def patient_list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT, Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    medicalinfoes = MedicalInfo.objects.filter(patient=request.user)
    # Page sorting.
    template_data['query'] = medicalinfoes.order_by('caseNumber')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'date':
            template_data['query'] = medicalinfoes.order_by('date')
        if request.GET['sort'] == 'caseNumber':
            template_data['query'] = medicalinfoes.order_by('caseNumber')    
        if request.GET['sort'] == 'patient':
            template_data['query'] = medicalinfoes.order_by('patient')
        if request.GET['sort'] == 'age':
            template_data['query'] = medicalinfoes.order_by('age') 
        if request.GET['sort'] == 'sex':
            template_data['query'] = medicalinfoes.order_by('sex')
        if request.GET['sort'] == 'civilStatus':
            template_data['query'] = medicalinfoes.order_by('civilStatus')
        if request.GET['sort'] == 'address':
            template_data['query'] = medicalinfoes.order_by('address')
        if request.GET['sort'] == 'temperature':
            template_data['query'] = medicalinfoes.order_by('temperature')
        if request.GET['sort'] == 'pulse':
            template_data['query'] = medicalinfoes.order_by('pulse') 
        if request.GET['sort'] == 'respiration':
            template_data['query'] = medicalinfoes.order_by('respiration')
        if request.GET['sort'] == 'bloodPressure':
            template_data['query'] = medicalinfoes.order_by('bloodPressure')    
        if request.GET['sort'] == 'bloodType':
            template_data['query'] = medicalinfoes.order_by('bloodType')
        if request.GET['sort'] == 'height':
            template_data['query'] = medicalinfoes.order_by('height')
        if request.GET['sort'] == 'weight':
            template_data['query'] = medicalinfoes.order_by('weight')
        if request.GET['sort'] == 'comments':
            template_data['query'] = medicalinfoes.order_by('comments')
    return render(request, 'Thesis/medicalinfo/patientlist.html', template_data)

def doctor_list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    medicalinfoes = MedicalInfo.objects.all()
    # Page sorting.
    template_data['query'] = medicalinfoes.order_by('caseNumber')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'date':
            template_data['query'] = medicalinfoes.order_by('date')
        if request.GET['sort'] == 'caseNumber':
            template_data['query'] = medicalinfoes.order_by('caseNumber')    
        if request.GET['sort'] == 'patient':
            template_data['query'] = medicalinfoes.order_by('patient')
        if request.GET['sort'] == 'age':
            template_data['query'] = medicalinfoes.order_by('age') 
        if request.GET['sort'] == 'sex':
            template_data['query'] = medicalinfoes.order_by('sex')
        if request.GET['sort'] == 'civilStatus':
            template_data['query'] = medicalinfoes.order_by('civilStatus')
        if request.GET['sort'] == 'address':
            template_data['query'] = medicalinfoes.order_by('address')
        if request.GET['sort'] == 'temperature':
            template_data['query'] = medicalinfoes.order_by('temperature')
        if request.GET['sort'] == 'pulse':
            template_data['query'] = medicalinfoes.order_by('pulse') 
        if request.GET['sort'] == 'respiration':
            template_data['query'] = medicalinfoes.order_by('respiration')
        if request.GET['sort'] == 'bloodPressure':
            template_data['query'] = medicalinfoes.order_by('bloodPressure')    
        if request.GET['sort'] == 'bloodType':
            template_data['query'] = medicalinfoes.order_by('bloodType')
        if request.GET['sort'] == 'height':
            template_data['query'] = medicalinfoes.order_by('height')
        if request.GET['sort'] == 'weight':
            template_data['query'] = medicalinfoes.order_by('weight')
        if request.GET['sort'] == 'comments':
            template_data['query'] = medicalinfoes.order_by('comments')
    
    return render(request, 'Thesis/medicalinfo/doctorlist.html', template_data)

def patient_history(request):

    query = MedicalInfo.objects.filter(Q(name=request.GET.get('search')))
    
    return render(request, 'Thesis/medicalinfo/doctorlist.html', {'query': query})

def update_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_PATIENT])
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