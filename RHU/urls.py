from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from RHU import views
from RHU import views_profile

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
   
    path('adminsignup/', views.register_view, name='adminregister'),
    path('doctorsignup/', views.doctor_signup_view),
    path('patientsignup/', views.patient_signup_view),

    path('adminlogin/', views.login_view, name='adminlogin'),
    path('doctorlogin/', LoginView.as_view(template_name='Thesis/doctorlogin.html')),
    path('patientlogin/', LoginView.as_view(template_name='Thesis/patientlogin.html')),

    path('profile/', views_profile.profile_view, name='profile'),

    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('patient-dashboard/', views.patient_dashboard_view,name='patient-dashboard'),

    

    path('afterlogin/', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='Thesis/index.html'),name='logout'),
    
]