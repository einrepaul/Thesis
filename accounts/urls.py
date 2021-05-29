from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminclick/', views.adminclick_view),
    path('doctorclick/', views.doctorclick_view),
    path('patientclick/', views.patientclick_view),
    path('adminsignup/', views.admin_signup_view),
    path('adminlogin/', LoginView.as_view(template_name='Thesis/adminlogin.html')),
    path('afterlogin/', views.afterlogin_view,name='afterlogin'),
    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),
    
]