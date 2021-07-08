from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('hospital-signup-form/', views.hospital_signup_form, name="hospital_signup_form"),
    path('get-hospitals/', views.fetch_hospital_list, name="hospital_list"),
]
