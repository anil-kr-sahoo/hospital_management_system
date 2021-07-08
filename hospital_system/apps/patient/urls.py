from django.urls import path, include
from . import views

urlpatterns = [
    path('patient-signup-form/', views.patient_signup_form, name="patient_signup_form"),

]
