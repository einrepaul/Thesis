from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminclick/', views.adminclick_view),
    path('doctorclick/', views.doctorclick_view),
    path('patientclick/', views.patientclick_view),

    path('adminsignup/', views.admin_signup_view),
    path('doctorsignup/', views.doctor_signup_view),
    path('patientsignup/', views.patient_signup_view),

    path('adminlogin/', LoginView.as_view(template_name='Thesis/adminlogin.html')),
    path('doctorlogin/', LoginView.as_view(template_name='Thesis/doctorlogin.html')),
    path('patientlogin/', LoginView.as_view(template_name='Thesis/patientlogin.html')),

   
    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('patient-dashboard/', views.patient_dashboard_view,name='patient-dashboard'),

    path('afterlogin/', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='Thesis/index.html'),name='logout'),
    
]