from .forms import PatientForm, AdminForm
from .models import Patient
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'Thesis/index.html')

def register(request):
    form = PatientForm()
    form = AdminForm()

    if request.method == 'POST' and 'b1' in request.POST:
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
    
     
    elif request.method == 'POST' and 'b2' in request.POST:
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
    
    context_dict = {'form': form}
    return render(request, 'Thesis/register.html', context_dict)

