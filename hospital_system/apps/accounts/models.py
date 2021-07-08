from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .manager import CustomUserManager

# Create your models here.

USER_SYSTEM_DETAILS = ['password', 'first_name', 'last_name', 'email', 'phone_number', 'role']


# [d.name for d in UserSystem._meta.get_fields()]


class UserRole:
    HOSPITAL = '1'
    DOCTOR = '2'
    PATIENT = '3'
    ROLES = (
        (HOSPITAL, "Hospital"),
        (DOCTOR, "Doctor"),
        (PATIENT, "Patient"))


class UserSystem(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=2, choices=UserRole.ROLES)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.'))
    object = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'first_name']
