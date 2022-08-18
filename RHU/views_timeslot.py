import logging
from tkinter import E

from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect

from RHU.forms import AppointmentForm, TimeSlotForm
from RHU.models import Action, Account, Appointment,  TimeSlot
from RHU import logger
from RHU import views

def timeslots(request):
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': 'Create'})
    default = {}
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        default['patient'] = request.user.account.pk
    elif request.user.account.role == Account.ACCOUNT_DOCTOR:
        default['doctor'] = request.user.account.pk
    request.POST._mutable = True
    request.POST.update(default)
    form = TimeSlotForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            slot = TimeSlot(
                startTime=form.cleaned_data['startTime'],
                endTime=form.cleaned_data['endTime'],
                end_date=form.cleaned_data['end_date'],
            )
            slot.save()
            logger.log(Action.ACTION_TIMESLOT, 'Time Slot created', request.user)
            form = TimeSlotForm(default)
            form._errors = {}
            template_data['alert_success'] = 'Successfully created your time slot!'
    else:
        form._errors = {}
    template_data['form'] = form
    return render(request, 'Thesis/timeslot/create.html', template_data)

