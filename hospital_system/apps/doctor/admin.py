from django.contrib import admin

# Register your models here.
from apps.doctor.models import Doctor


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'hospital', 'email', 'phone_number')
    search_fields = ['hospital__name', 'email', 'first_name', 'last_name', 'phone_number']


admin.site.register(Doctor, DoctorAdmin)
