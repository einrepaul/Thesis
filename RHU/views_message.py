from itertools import chain
import logging
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect

from RHU.models import Message
from RHU import logger
from RHU.forms import MessageForm
from RHU.models import Account,  Action
from RHU import views
from django.db.models import Q

console_logger = logging.getLogger(__name__) 

def patient_list_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    messages = Message.objects.filter(Q(sender=request.user.account) | Q(target=request.user.account))
    template_data['query'] = messages.order_by('timestamp')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'to':
            template_data['query'] = messages.order_by('target_profile', 'timestamp')
        if request.GET['sort'] == 'from':
            template_data['query'] = messages.order_by('sender_profile', 'timestamp')
        if request.GET['sort'] == 'subject':
            template_data['query'] = messages.order_by('header', 'timestamp')
        if request.GET['sort'] == 'time':
            template_data['query'] = messages.order_by('timestamp')
        if request.GET['sort'] == 'read':
            template_data['query'] = messages.order_by('read', 'timestamp')
    return render(request, 'Thesis/message/patientlist.html', template_data)

def doctor_list_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    messages = Message.objects.filter(Q(sender=request.user.account) | Q(target=request.user.account))
    template_data['query'] = messages.order_by('timestamp')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'to':
            template_data['query'] = messages.order_by('target_profile', 'timestamp')
        if request.GET['sort'] == 'from':
            template_data['query'] = messages.order_by('sender_profile', 'timestamp')
        if request.GET['sort'] == 'subject':
            template_data['query'] = messages.order_by('header', 'timestamp')
        if request.GET['sort'] == 'time':
            template_data['query'] = messages.order_by('timestamp')
        if request.GET['sort'] == 'read':
            template_data['query'] = messages.order_by('read', 'timestamp')
    return render(request, 'Thesis/message/doctorlist.html', template_data) 

def admin_list_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    messages = Message.objects.filter(Q(sender=request.user.account) | Q(target=request.user.account))
    template_data['query'] = messages.order_by('timestamp')
    if 'sort' in request.GET:
        if request.GET['sort'] == 'to':
            template_data['query'] = messages.order_by('target_profile', 'timestamp')
        if request.GET['sort'] == 'from':
            template_data['query'] = messages.order_by('sender_profile', 'timestamp')
        if request.GET['sort'] == 'subject':
            template_data['query'] = messages.order_by('header', 'timestamp')
        if request.GET['sort'] == 'time':
            template_data['query'] = messages.order_by('timestamp')
        if request.GET['sort'] == 'read':
            template_data['query'] = messages.order_by('read', 'timestamp')
    return render(request, 'Thesis/message/adminlist.html', template_data)