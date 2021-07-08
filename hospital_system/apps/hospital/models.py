from django.db import models
from django.utils.translation import ugettext_lazy as _

HOSPITAL_DETAILS = ['name', 'email', 'phone_number', 'address',
                    'reg_number', 'established_date', 'details']


# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    reg_number = models.CharField(max_length=100, null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)
    details = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_doctor_list(self, context=dict()):
        context['doctors'] = list()
        from apps.doctor.models import Doctor
        all_doctors = Doctor.objects.filter(hospital__email=self.email)
        for i, doctor in enumerate(all_doctors):
            details = dict()
            details['sl_no'] = str(i + 1)
            details['full_name'] = doctor.get_full_name()
            details['email'] = doctor.get_email()
            details['phone_no'] = doctor.get_phone_number()
            details['gender'] = doctor.get_gender_display() if doctor.gender else '-'
            context['doctors'].append(details)
        return context
