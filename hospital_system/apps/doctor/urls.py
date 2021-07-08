from django.urls import path, include
from . import views

urlpatterns = [
    path('doctor-signup-form/', views.doctor_signup_form, name="doctor_signup_form"),
]
