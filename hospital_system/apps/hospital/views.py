from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework.decorators import api_view

from apps.hospital.models import Hospital


def home_page(request):
    return render(request, 'index.html', context={})


# @api_view(['GET'])
def hospital_signup_form(request):
    return render(request, 'signup.html', context={"hospital_type": True})


def fetch_hospital_list(request):
    if 'logged_email' in request.session:
        return HttpResponseRedirect('/accounts/account-login/')
    hospitals = list(Hospital.objects.all())
    all_hospitals = list()
    for data in hospitals:
        context = dict()
        context['name'] = data.name[:15] + '..' if len(data.name) > 15 else data.name
        context['address'] = data.address[:35] + '..' if len(data.address) > 35 else data.address
        all_hospitals.append(context)
    return render(request, 'hospital.html', {'hospitals': all_hospitals})
