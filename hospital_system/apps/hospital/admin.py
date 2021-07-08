from django.contrib import admin

# Register your models here.
from apps.hospital.models import Hospital


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address')
    search_fields = ['name', 'email', 'phone_number']


admin.site.register(Hospital, HospitalAdmin)
