from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from django.utils import timezone
import datetime

# Clinical trial effort instance model
class CTEffort(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    estimated_accruals = models.IntegerField(blank=True, null=True)
    pi_effort = models.FloatField(blank=True, null=True)
    pi_effort_copy = models.BooleanField(default=False)
    monitor_days = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'effort_models'


# Cycle types model
class CycleTypes(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cycle_types'


# Personnel types model
class PersonnelTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'personnel_types'


# Complexity types model
# class ComplexityTypes(models.Model):
#     id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=32, blank=True, null=True)
#     name = models.CharField(max_length=32, blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'complexity_types'


# Trial arms model
class TrialArms(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    name = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trial_arms'

# Cycles model
class Cycles(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    arm = models.ForeignKey('TrialArms',on_delete=models.CASCADE, null=True)
    type = models.ForeignKey('CycleTypes',on_delete=models.CASCADE,)
    number_cycles = models.IntegerField(blank=True, null=True, default=1)
    number_visits = models.IntegerField(blank=True, null=True, default=1)
    name = models.CharField(max_length=32, blank=True, null=True)
    copy_hours = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cycles'

# Visits model
class Visits(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    cycle = models.ForeignKey('Cycles',on_delete=models.CASCADE,)
    cycle_number = models.IntegerField(blank=True, null=True)
    visit_number = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'visits'


# Personnel model
class Personnel(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    type = models.ForeignKey('PersonnelTypes',on_delete=models.CASCADE,)
    name = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'visit_personnel'


# Clinical research coordinator visit model
class CRCVisit(models.Model):
    id = models.AutoField(primary_key=True)
    visit = models.ForeignKey('Visits',on_delete=models.CASCADE,null=True)
    calendar_screen = models.FloatField(blank=True, null=True, default=0)
    chart_review = models.FloatField(blank=True, null=True, default=0)
    pre_cert = models.FloatField(blank=True, null=True, default=0)
    consent = models.FloatField(blank=True, null=True, default=0)
    eligibility_checklist = models.FloatField(blank=True, null=True, default=0)
    registration = models.FloatField(blank=True, null=True, default=0)
    ivrs_iwrs = models.FloatField(blank=True, null=True, default=0)
    scheduling = models.FloatField(blank=True, null=True, default=0)
    medical_history = models.FloatField(blank=True, null=True, default=0)
    vitals = models.FloatField(blank=True, null=True, default=0)
    lab_work = models.FloatField(blank=True, null=True, default=0)
    imaging = models.FloatField(blank=True, null=True, default=0)
    ecgs = models.FloatField(blank=True, null=True, default=0)
    oral_medication = models.FloatField(blank=True, null=True, default=0)
    clinic_notes = models.FloatField(blank=True, null=True, default=0)
    billing = models.FloatField(blank=True, null=True, default=0)
    crf_entry = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'crc_visit'

# Nurse coordinator visit model
class NCVisit(models.Model):
    id = models.AutoField(primary_key=True)
    visit = models.ForeignKey('Visits',on_delete=models.CASCADE,null=True)
    infusion = models.FloatField(blank=True, null=True, default=0)
    pk_samples = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'nc_visit'


# Data coordinator visit model
class DCVisit(models.Model):
    id = models.AutoField(primary_key=True)
    visit = models.ForeignKey('Visits',on_delete=models.CASCADE,null=True)
    infusion = models.FloatField(blank=True, null=True, default=0)
    pk_samples = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'dc_visit'


# General visit model
class GeneralVisit(models.Model):
    id = models.AutoField(primary_key=True)
    visit = models.ForeignKey('Visits',on_delete=models.CASCADE,null=True)
    training = models.FloatField(blank=True, null=True, default=0)
    protocol_review = models.FloatField(blank=True, null=True, default=0)
    source_document = models.FloatField(blank=True, null=True, default=0)
    regulatory = models.FloatField(blank=True, null=True, default=0)
    sponsor_meetings = models.FloatField(blank=True, null=True, default=0)
    internal_meetings = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'g_visit'


# Complexity model
# class Complexity(models.Model):
#     id = models.AutoField(primary_key=True)
#     instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
#
#
#     class Meta:
#         managed = True
#         db_table = 'g_visit'


# Complexity value model
# class ComplexityValue(models.Model):
#     id = models.AutoField(primary_key=True)
#     complexity = models.ForeignKey('Complexity',on_delete=models.CASCADE,)
#     type = models.ForeignKey('ComplexityTypes',on_delete=models.CASCADE,)
#     value = models.IntegerField(blank=True, null=True, default=0, min_value=0, max_value=3)
#
#
#     class Meta:
#         managed = True
#         db_table = 'g_visit'
