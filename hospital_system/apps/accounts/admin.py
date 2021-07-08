from apps.accounts.models import UserSystem
from django.contrib import admin


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'email', 'phone_number')
    search_fields = ['role', 'email', 'phone_number']


admin.site.register(UserSystem, UserAdmin)
