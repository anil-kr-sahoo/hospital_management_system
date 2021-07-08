from django.db import models

# Create your models here.
from apps.hospital.models import Hospital
from django.utils.translation import ugettext_lazy as _

DOCTOR_DETAILS = ['first_name', 'last_name', 'hospital',
                  'email', 'phone_number', 'gender', 'details']

GENDER = (
    ('1', 'Male'),
    ('2', 'Female'),
    ('3', 'Transgender'),
    ('4', 'Unknown')
)


class Doctor(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    email = models.EmailField(_('email address'), null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER, blank=True, null=True)
    details = models.CharField(max_length=500, null=True, blank=True)

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

    def get_patient_list(self, context=dict()):
        context['patients'] = list()
        from apps.patient.models import Patient
        all_patients = Patient.objects.filter(doctor__email=self.email).order_by('appointment_date')
        for i, patient in enumerate(all_patients):
            details = dict()
            details['sl_no'] = str(i + 1)
            details['full_name'] = patient.get_full_name()
            details['appointment'] = patient.get_appointment_date()
            details['prescription'] = patient.get_prescriptions()[:20] + '..' if len(
                patient.get_prescriptions()) > 20 else patient.get_prescriptions()
            details['blood'] = patient.get_blood_group_display() if patient.blood_group else '-'
            context['patients'].append(details)
        return context
