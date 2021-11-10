import logging
import csv 
import io

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.contrib import messages

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

def admin_list_view(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    if request.user.account.role == Account.ACCOUNT_ADMIN:
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
    return render(request, 'Thesis/medtest/adminlist.html', template_data)

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

class import_data_csv(View):
    template_name = 'Thesis/medtest/patientlist.html'

    def get(self, request, *args, **kwargs):
        data = MedicalTest.objects.all().values_list('doctor', 'patient', 'name', 'date', 'status')
        return render(request, self.template_name, {"data":data})

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
                obj, created = MedicalTest.objects.update_or_create(
                    doctor=col[0], patient=col[1], name=col[2], date=col[3], status=col[4])
        data = MedicalTest.objects.all().values_list('doctor', 'patient', 'name', 'date', 'status')
        return render(request, self.template_name, {"data": data})
                
class export_data_csv(View):
    def get(self, request, *args, **kwargs):
        data = MedicalTest.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['doctor', 'patient', 'name', 'date', 'status'])
        for obj in data:
            writer.writerow([obj.doctor.account.profile, obj.patient.account.profile, obj.name, obj.date, obj.completed])
        return response
