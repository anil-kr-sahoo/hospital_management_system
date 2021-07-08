from django.contrib import admin

# Register your models here.
from apps.patient.models import Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'hospital', 'doctor', 'email', 'phone_number')
    search_fields = ['hospital__name', 'doctor__first_name', 'doctor__last_name', 'email', 'first_name', 'last_name',
                     'phone_number']


admin.site.register(Patient, PatientAdmin)
