import requests
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from hospital_system.settings import SCHEME, ALLOWED_HOSTS
from .models import UserSystem
from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializer import LoginSerializer, UserSerializer, InsertionSerializer
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
from ..doctor.models import DOCTOR_DETAILS, Doctor
from ..hospital.models import HOSPITAL_DETAILS, Hospital
from ..patient.models import PATIENT_DETAILS, Patient


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        signup_data = {k: v for k, v in request.data.items() if v}
        serializer = UserSerializer(data=signup_data)
        if serializer.is_valid():
            data = {k: v for k, v in request.data.items() if v}
            insert_serializer = InsertionSerializer(data=request.data)
            if insert_serializer.is_valid():
                assign_role_wise(**data)
                serializer.save()
                return Response({"msg": "Data Inserted Successfully"}, status=status.HTTP_200_OK)
            return Response(insert_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.data
            try:
                retrive_email = UserSystem.object.get(email=user_data['email'])
                if not (retrive_email.check_password(user_data['password'])):
                    return Response({'AuthenticationFailed': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                raise AuthenticationFailed('Incorrect Email')
            return Response({"msg": "Logged In Successfully"}, status=status.HTTP_200_OK)
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def assign_role_wise(**kwargs):
    role = kwargs.get('role')
    if role == '1':
        context = dict()
        for data in HOSPITAL_DETAILS:
            context[data] = kwargs.get("first_name") if data == "name" else kwargs.get(data)
        Hospital.objects.create(**context)
    if role == '2':
        context = dict()
        try:
            hospital = Hospital.objects.get(email=kwargs.get('logged_email'))
            kwargs['hospital'] = hospital
            for data in DOCTOR_DETAILS:
                context[data] = kwargs.get(data)
            Doctor.objects.create(**context)
        except Exception as e:
            print(e)
            raise Exception("Unable to create Doctor")

    if role == '3':
        context = dict()
        try:
            doctor = Doctor.objects.get(email=kwargs.get('logged_email'))
            kwargs['doctor'] = doctor
            kwargs['hospital'] = doctor.hospital
            for data in PATIENT_DETAILS:
                context[data] = kwargs.get(data)
            Patient.objects.create(**context)
        except Exception as e:
            print(e)
            raise Exception("Unable to create Patient")


def login_page(request):
    if 'logged_email' in request.session:
        return HttpResponseRedirect('/accounts/account-login/')
    return render(request, 'login.html')


def logout_page(request):
    if 'logged_email' in request.session:
        del request.session['logged_email']
    if 'user_name' in request.session:
        del request.session['user_name']
    return HttpResponseRedirect('/hospital')


def account_signup(request):
    if request.method == 'POST':
        context = {'status': True}
        try:
            if request.POST['password'] != request.POST['c_password']:
                context["message"] = "Please match the password and confirm password"
                raise Exception("Password miss match")
            if '+' in request.POST['phone_number']:
                mob = request.POST['phone_number'].split('+')[1]
                if len(mob) != 12 or not all([data.isnumeric() for data in mob]):
                    context["message"] = "Please provide valid phone number"
                    raise Exception("Invalid Phone number")
            else:
                mob = request.POST['phone_number']
                if not all([data.isnumeric() for data in mob]):
                    context["message"] = "Please provide valid phone number"
                    raise Exception("Invalid Phone number")
            r = requests.post(SCHEME + '://' + ALLOWED_HOSTS[0] + '/accounts/signup/', params=request.POST,
                              data=request.POST)
            if r.status_code == 200:
                context["message"] = 'Data Added Successfully'
            if r.status_code == 400:
                context["message"] = list(r.json().values())[0][0]
        except Exception as e:
            pass
        if 'logged_email' in request.session:
            return render(request, 'signup.html', context=context)
        else:
            context['home'] = True
            return render(request, 'signup.html', context=context)


def account_login(request):
    if 'logged_email' in request.session:
        context, logged_email, user_name = login_redirection(email=request.session['logged_email'])
        if logged_email and user_name:
            request.session['logged_email'] = logged_email
            request.session['user_name'] = user_name
        return render(request, 'lists.html', context=context)
    if request.method == 'POST':
        data = request.POST
        r = requests.post(SCHEME + '://' + ALLOWED_HOSTS[0] + '/accounts/login/', params=request.POST, data=data)
        if r.status_code == 200:
            try:
                context, logged_email, user_name = login_redirection(email=data.get('email'))
                if logged_email and user_name:
                    request.session['logged_email'] = logged_email
                    request.session['user_name'] = user_name
                return render(request, 'lists.html', context=context)
            except Exception as e:
                print(e)
                context = {"status": True, "message": "Unable to logged in, Please try again"}
                return render(request, 'login.html', context=context)
        elif r.status_code == 400:
            context = {"status": True, "message": r.json().get('AuthenticationFailed')}
            return render(request, 'login.html', context=context)
    context = {"status": True, "message": "Unable to logged in, Please try again"}
    return render(request, 'login.html', context=context)


def login_redirection(**kwargs):
    email = kwargs.get('email')
    get_user = UserSystem.object.get(email=email)
    if get_user.role == "1":
        context = dict()
        hospital = Hospital.objects.get(email=email)
        context['hospital_name'] = hospital.name
        context['hospital_type'] = True
        context = hospital.get_doctor_list(context=context)
        logged_email = hospital.email
        user_name = get_user.first_name
        return context, logged_email, user_name
    elif get_user.role == "2":
        context = dict()
        doctor = Doctor.objects.filter(email=email).last()
        context['doctor_name'] = doctor.get_full_name()
        context['doctor_type'] = True
        context = doctor.get_patient_list(context=context)
        logged_email = doctor.email
        user_name = get_user.first_name
        return context, logged_email, user_name
    elif get_user.role == "3":
        context = dict()
        patient = Patient.objects.filter(email=email).last()
        context['patient_name'] = patient.get_full_name()
        context['patient_type'] = True
        context = patient.get_visit_details(context=context)
        logged_email = patient.email
        user_name = get_user.first_name
        return context, logged_email, user_name
