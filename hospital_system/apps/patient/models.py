from django.db import models

# Create your models here.
from apps.doctor.models import Doctor, GENDER
from apps.hospital.models import Hospital
from django.utils.translation import ugettext_lazy as _

PATIENT_DETAILS = ['first_name', 'last_name', 'hospital', 'doctor', 'email', 'phone_number',
                   'gender', 'blood_group', 'appointment_date', 'prescription']

BLOOD = (
    ('1', 'A +'),
    ('2', 'A -'),
    ('3', 'B +'),
    ('4', 'B -'),
    ('5', 'O +'),
    ('6', 'O -'),
    ('7', 'AB +'),
    ('8', 'AB -')
)


class Patient(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(_('email address'), null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER, blank=True, null=True)
    blood_group = models.CharField(max_length=2, choices=BLOOD, blank=True, null=True)
    appointment_date = models.DateField(blank=True, null=True)
    prescription = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)

    def get_full_name(self):
        full_name = ''
        try:
            full_name = self.first_name + " " + self.last_name if self.last_name else self.first_name
        except Exception as e:
            pass
        return full_name

    def get_email(self):
        email = ''
        try:
            email = self.email if self.email else ''
        except Exception as e:
            pass
        return email

    def get_phone_number(self):
        phone = ''
        try:
            phone = self.phone_number if self.phone_number else ''
        except Exception as e:
            pass
        return phone

    def get_appointment_date(self):
        appointment = ''
        try:
            appointment = self.appointment_date if self.appointment_date else ''
        except Exception as e:
            pass
        return appointment

    def get_prescriptions(self):
        prescription = ''
        try:
            prescription = self.prescription if self.prescription else ''
        except Exception as e:
            pass
        return prescription

    def get_visit_details(self, context=dict()):
        context['visits'] = list()
        all_patients = Patient.objects.filter(email=self.email).order_by('appointment_date')
        for i, patient in enumerate(all_patients):
            details = dict()
            details['sl_no'] = str(i + 1)
            details['hospital'] = patient.hospital.name[:10] +'..' if len(
                patient.hospital.name) > 10 else patient.hospital.name
            details['doctor'] = patient.doctor.get_full_name()[:10] +'..' if len(
                patient.doctor.get_full_name()) > 10 else patient.doctor.get_full_name()
            details['appointment_date'] = patient.appointment_date
            details['prescription'] = patient.get_prescriptions()[:20] +'..' if len(
                patient.get_prescriptions()) > 20 else patient.get_prescriptions()
            context['visits'].append(details)
        return context


def initialize_table_creation(**kwargs):
    """
    This function helps to insert data in database
    :return:
    """
    doctor_list = kwargs.get('doctor_list')
    pat_email = kwargs.get('email')

    pat = Patient.objects.filter(email=pat_email).first()  # give patient email here

    context = {"first_name": pat.first_name, "last_name": pat.last_name,
               "email": pat.email, "phone_number": pat.phone_number,
               "gender": pat.gender, "blood_group": pat.blood_group}

    for data in doctor_list:
        try:
            doctor = Doctor.objects.get(email=data.get('doctor'))
        except Exception as e:
            print("No registered doctor found with email '" + data.get('doctor') + "'")
            continue

        appointment_date = data.get('appointment_date', '') if data.get('appointment_date', '') else None
        prescription = data.get('prescription', '') if data.get('prescription', '') else None
        context["doctor"] = doctor
        context["hospital"] = doctor.hospital
        context['appointment_date'] = appointment_date
        context['prescription'] = prescription
        if Patient.objects.filter(doctor=doctor, email=pat_email,
                                  appointment_date=data.get('appointment_date', '')).exists():
            print("Unable to create data, as patient visit already fixed with doctor '" + doctor.get_full_name()
                  + "' with same appointment date '" + str(appointment_date) + "'")
            continue

        try:
            Patient.objects.create(**context)
            print("Data created Successfully")
        except Exception as e:
            print("Unable to create Patient", e)
