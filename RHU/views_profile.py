import logging

from django.shortcuts import render
from django.contrib.auth import authenticate

from RHU import views

console_logger = logging.getLogger(__name__) 

def profile_view(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request)
    return render(request, 'Thesis/profile.html', template_data)