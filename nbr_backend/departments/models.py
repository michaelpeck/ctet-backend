from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from django.utils import timezone
from datetime import datetime

# Department model
class Departments(models.Model):
    dept_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'departments'

# Support contacts model
class SupportContacts(models.Model):
    contact_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=32, blank=True, null=True)
    department = models.ForeignKey('Departments',on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'support_contacts'

# Support request model
class SupportRequests(models.Model):
    request_id = models.AutoField(primary_key=True)
    department = models.ForeignKey('Departments',on_delete=models.CASCADE, null=True)
    contact = models.ForeignKey('SupportContacts',on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    subject = models.CharField(max_length=64, blank=True, null=True)
    message = models.CharField(max_length=1500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'support_requests'
