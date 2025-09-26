from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', views.signup, name='Sign Up'),
     path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('',views.homepage, name='Home'),
    path('patient', views.patient_list, name='Patient List'),
    path('profile/complete/', views.complete_profile, name='complete_profile'),
    path('patient/create/', views.create_patient, name='Create Patient'),
    path('patient/<slug:slug>/', views.patient_detail, name='Patient Detail'),
    path('doctor/create/', views.create_doctor, name='Create Doctor'),
    path('doctor/<slug:slug>/', views.doctor_detail, name='Doctor Detail'),
    path("doctor", views.doctor_list, name="Doctor List"),
    path('patient/<slug:slug>/report/upload/', views.upload_medical_report, name='Upload Medical Report'),
    path('patient/<slug:slug>/record/create/', views.create_medical_record, name='Create Medical Record'),
    path('patient/<slug:slug>/medications/', views.medication_list, name='Medication List'),
    path('patient/<slug:slug>/medications/add/', views.add_medication, name='Add Medication'),
]