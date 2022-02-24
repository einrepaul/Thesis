import logging
import csv
import io

from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from RHU.forms import MedicalInfoForm
from RHU.models import Action, Account, MedicalInfo
from RHU import logger
from RHU import views

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
    template_data['query'] = medicalinfoes.order_by('patient_id')
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

def doctor_search_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_DOCTOR])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    medicalinfoes = MedicalInfo.objects.all()
    # Page sorting.
    template_data['query'] = medicalinfoes.order_by('patient_id')
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
    
    return render(request, 'Thesis/medicalinfo/patienthistory.html', template_data)

def patient_history(request): 

    query = MedicalInfo.objects.filter(Q(patient_id=request.GET.get('search')) |  
                                       Q(caseNumber=request.GET.get('search')) |  
                                       Q(age=request.GET.get('search')) |
                                       Q(sex=request.GET.get('search')) |
                                       Q(civilStatus=request.GET.get('search')) |
                                       Q(barangay=request.GET.get('search')) |
                                       Q(temperature=request.GET.get('search')) |
                                       Q(pulse=request.GET.get('search')) |
                                       Q(respiration=request.GET.get('search')) |
                                       Q(bloodPressure=request.GET.get('search')) |
                                       Q(bloodType=request.GET.get('search')) |
                                       Q(height=request.GET.get('search')) |
                                       Q(weight=request.GET.get('search')) |
                                       Q(comments__icontains=request.GET.get('search')))
    
    return render(request, 'Thesis/medicalinfo/patienthistory.html', {'query': query})

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

class import_data_csv(View):
    template_name = 'Thesis/medicalinfo/doctorlist.html'

    def get(self, request, *args, **kwargs):
        query = MedicalInfo.objects.all().values_list('patient_id','date', 'caseNumber', 'patient.account.profile', 'age', 'sex', 'civilStatus', 'barangay', 'temperature', 'pulse', 'respiration', 'bloodPressure', 'bloodType', 'height', 'weight', 'comments')
        return render(request, self.template_name, {"query":query})

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['file']
        print(csv_file.name)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File Must Be in CSV Format')
        else:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for col in csv.reader(io_string, delimiter=',', quotechar="|"):
                obj, created = MedicalInfo.objects.update_or_create(
                   patient_id=[0], date=col[1], caseNumber=col[2], patient=col[3], age=col[4], sex=col[5], civilStatus=col[6], barangay=col[7], temperature=col[8], pulse=col[9], respiration=col[10], bloodPressure=col[11], bloodType=col[12], height=col[13], weight=col[14], comments=[15])
        query = MedicalInfo.objects.all().values_list('patient_id', 'date', 'caseNumber', 'patient', 'age', 'sex', 'civilStatus', 'barangay', 'temperature', 'pulse', 'respiration', 'bloodPressure', 'bloodType', 'height', 'weight', 'comments')
        return render(request, self.template_name, {"query": query})
                
class export_data_csv(View):
    def get(self, request, *args, **kwargs):
        data = MedicalInfo.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="medicalinfo.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['id', 'date', 'caseNumber', 'patient', 'age', 'sex', 'civilStatus', 'barangay', 'temperature', 'pulse', 'respiration', 'bloodPressure', 'bloodType', 'height', 'weight', 'comments'])
        for obj in data:
            writer.writerow([obj.patient_id, obj.date, obj.caseNumber, obj.patient.account.profile, obj.age, obj.sex, obj.civilStatus, obj.barangay, obj.temperature, obj.pulse, obj.respiration, obj.bloodPressure, obj.bloodType, obj.height, obj.weight, obj.comments])
        return response
