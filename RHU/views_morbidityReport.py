import logging
import csv 

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from RHU.forms import MorbidityReportForm
from RHU.models import MorbidityReport, Account, Action
from RHU import logger
from RHU import views

console_logger = logging.getLogger(__name__)

def create_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Update"})
    # Proceed with the rest of the view
    default = {}
    if request.user.account.role == Account.ACCOUNT_ADMIN:
        default['admin'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = MorbidityReportForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            morbidityreport = MorbidityReport(
                barangay=form.cleaned_data['barangay'],
                disease=form.cleaned_data['disease'],
                classification=form.cleaned_data['classification'],
                cases=form.cleaned_data['cases'],
            )
            morbidityreport.save()
            logger.log(Action.ACTION_MORBIDITYREPORT, 'Morbidity Report updated', request.user)
            form = MorbidityReportForm(default)  # Clean the form when the page is redisplayed
            form._errors = {}
            template_data['alert_success'] = "Successfully updated the morbidity report!"
            return HttpResponseRedirect('/download_report')
    else:
        form._errors = {}
    # if request.user.account.role == Account.ACCOUNT_DOCTOR:
    # form.disable_field('performedBy')
    template_data['form'] = form
    return render(request, 'Thesis/morbidityreport/create.html', template_data)

def list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': 'Save'})
    # Proceed with the rest of the view
    morbidityreports = MorbidityReport.objects.all()
    # Page sorting.
    template_data['query'] = morbidityreports.order_by('barangay')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'barangay':
            template_data['query'] = morbidityreports.order_by('barangay')
        if request.GET['sort'] == 'disease':
            template_data['query'] = morbidityreports.order_by('disease')
        if request.GET['sort'] == 'classification':
            template_data['query'] = morbidityreports.order_by('classification')
        if request.GET['sort'] == 'cases':
            template_data['query'] = morbidityreports.order_by('cases')   
    return render(request, 'Thesis/morbidityreport/list.html', template_data)

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reports.csv"'

    writer = csv.writer(response)
    writer.writerow(['barangay', 'disease','classification','cases','latitude','longitude'])

    reports = MorbidityReport.objects.all().values_list('barangay','disease','classification','cases','latitude','longitude')
    for report in reports:
        writer.writerow(report)

    return response