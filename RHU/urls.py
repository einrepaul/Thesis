from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from RHU import views
from RHU import views_profile
from RHU import views_message
from RHU import views_medicalInfo
from RHU import views_appointment
from RHU import views_medtest
from RHU import views_prescription
from RHU import views_admin
from RHU import views_heatmap
from RHU import views_morbidityReport
#from RHU import views_timeslot

app_name='RHU'

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
   
    path('adminsignup/', views.admin_register_view, name='adminregister'),
    path('doctorsignup/', views.doctor_register_view, name='doctorsignup'),
    path('patientsignup/', views.patient_register_view, name='patientsignup'),

    path('adminlogin/', views.admin_login_view, name='adminlogin'),
    path('doctorlogin/', views.doctor_login_view, name='doctorlogin'),
    path('patientlogin/', views.patient_login_view, name='patientlogin'),
    path('afterlogin/', views.afterlogin_view,name='afterlogin'),
    
    path('patient_profile/', views_profile.patient_profile_view, name='patientprofile'),
    path('admin_profile/', views_profile.admin_profile_view, name='adminprofile'),
    path('doctor_profile/', views_profile.doctor_profile_view, name='doctorprofile'),

    path('patient_profile/password/', views_profile.patient_password_view, name='patientpassword'),
    path('doctor_profile/password/', views_profile.doctor_password_view, name='doctorpassword'),
    path('admin_profile/password/', views_profile.admin_password_view, name='adminpassword'),

    path('patient_profile/update/', views_profile.patient_update_view, name='patientupdate'),
    path('doctor_profile/update/', views_profile.doctor_update_view, name='doctorupdate'),
    path('admin_profile/update/', views_profile.admin_update_view, name='adminupdate'),

    path('patient_profile/message/list/', views_message.patient_list_view, name='message/patientlist'),
    path('doctor_profile/message/list/', views_message.doctor_list_view, name='message/doctorlist'),
    path('admin_profile/message/list/', views_message.admin_list_view, name='message/adminlist'),

    path('medicalinfo/patient/', views_medicalInfo.patient_view, name='medicalinfo/patient'),
    path('medicalinfo/create/', views_medicalInfo.patient_view, name='medicalinfo/create'),
    path('patient_profile/medicalinfo/list/', views_medicalInfo.patient_list_view, name='medicalinfo/patientlist'),
    path('doctor_profile/medicalinfo/list/', views_medicalInfo.doctor_list_view, name='medicalinfo/doctorlist'),
    path('doctor_profile/medicalinfo/search/', views_medicalInfo.doctor_search_view, name='medicalinfo/doctorsearch'),
    path('doctor_profile/medicalinfo/search/search', views_medicalInfo.patient_history, name='medicalinfo/patienthistory'),
    path('medicalinfo/update/', views_medicalInfo.update_view, name='medicalinfo/update'),

    path('patient_profile/appointment/create/', views_appointment.patient_create_view, name='appointment/create'),
    path('doctor_profile/appointment/create/', views_appointment.doctor_create_view, name='appointment/create'),

    path('patient_profile/appointment/list/', views_appointment.patient_list_view, name='appointment/patientlist'),
    path('doctor_profile/appointment/list/', views_appointment.doctor_list_view, name='appointment/doctorlist'),
    path('admin_profile/appointment/list/', views_appointment.admin_list_view, name='appointment/adminlist'),

    path('patient_profile/appointment/patientupdate', views_appointment.patient_update_view, name='appointment/patientupdate'),

    path('patient_profile/appointment/approve', views_appointment.admin_approve_appointment, name='appointment/approve'),
    
    path('patient_profile/medtest/list', views_medtest.patient_list_view, name='medtest/patientlist'),
    path('doctor_profile/medtest/list', views_medtest.doctor_list_view, name='medtest/doctorlist'),
    path('admin_profile/medtest/list', views_medtest.admin_list_view, name='medtest/adminlist'),
    path('medtest/upload/', views_medtest.create_view, name='medtest/upload'),

    path('patient_profile/prescription/list', views_prescription.patient_list_view, name='prescription/patientlist'),
    path('doctor_profile/prescription/list', views_prescription.doctor_list_view, name='prescription/doctorlist'),
    path('prescription/create', views_prescription.create_view, name='prescription/create'),

    path('patient_profile/heatmap/', views_heatmap.heatmap, name='patientheatmap'),
    path('doctor_profile/heatmap', views_heatmap.heatmap, name='doctorheatmap'),
    path('admin_profile/heatmap', views_heatmap.heatmap, name='adminheatmap'),

    path('report/', views_morbidityReport.create_view, name='morbidityreport/create'),
    path('report/list', views_morbidityReport.list_view, name='morbidityreport/list'),
    path('doctor_profile/report/', views_morbidityReport.doctor_create_view, name='morbidityreport/doctorcreate'),
    path('doctor_profile/report/list', views_morbidityReport.doctor_list_view, name='morbidityreport/doctorlist'),

    path('error/patientdenied/', views.patient_error_denied_view, name='error/patientdenied'),
    path('error/doctordenied/', views.doctor_error_denied_view, name='error/doctordenied'),
    path('error/admindenied/', views.admin_error_denied_view, name='error/admindenied'),
    
    path('admin_profile/appointment/approve/', views_appointment.admin_approve_appointment, name='admin-appointment-approve'),
    #path('admin_profile/timeslots/', views_timeslot.timeslots, name='admin/createtimeslots'),
    path('admin_profile/admin/users/', views_admin.users_view, name='admin/users'),
    path('admin_profile/admin/activity/', views_admin.activity_view, name='admin/activity'),
    path('admin_profile/admin/stats/', views_admin.statistic_view, name='admin/stats'),
    path('admin_profile/admin/createemployee/', views_admin.createemployee_view, name='admin/createemployee'),

    path('approve-appointment/<int:pk>', views_appointment.approve_appointment_view, name='approve-appointment'),
    path('reject-appointment/<int:pk>', views_appointment.reject_appointment_view,name='reject-appointment'),
]