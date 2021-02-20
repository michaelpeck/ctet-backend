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
    cte_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
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
    ct_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cycle_types'


# Personnel types model
class PersonnelTypes(models.Model):
    pt_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'personnel_types'


# Trial arms model
class TrialArms(models.Model):
    ta_id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    name = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trial_arms'

# Cycles model
class Cycles(models.Model):
    c_id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    arm = models.ForeignKey('TrialArms',on_delete=models.CASCADE,)
    number_visits = models.IntegerField(blank=True, null=True)
    heading = models.CharField(max_length=32, blank=True, null=True)
    copy_hours = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cycles'

# Visits model
class Visits(models.Model):
    v_id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    arm = models.ForeignKey('TrialArms',on_delete=models.CASCADE,)
    cycle = models.ForeignKey('Cycles',on_delete=models.CASCADE,)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'visits'


# Personnel model
class Personnel(models.Model):
    p_id = models.AutoField(primary_key=True)
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
    crc_id = models.AutoField(primary_key=True)
    calendar_screen = models.FloatField(blank=True, null=True)
    chart_review = models.FloatField(blank=True, null=True)
    pre_cert = models.FloatField(blank=True, null=True)
    consent = models.FloatField(blank=True, null=True)
    eligibility_checklist = models.FloatField(blank=True, null=True)
    registration = models.FloatField(blank=True, null=True)
    ivrs_iwrs = models.FloatField(blank=True, null=True)
    scheduling = models.FloatField(blank=True, null=True)
    medical_history = models.FloatField(blank=True, null=True)
    vitals = models.FloatField(blank=True, null=True)
    lab_work = models.FloatField(blank=True, null=True)
    imaging = models.FloatField(blank=True, null=True)
    ecgs = models.FloatField(blank=True, null=True)
    oral_medication = models.FloatField(blank=True, null=True)
    clinic_notes = models.FloatField(blank=True, null=True)
    billing = models.FloatField(blank=True, null=True)
    crf_entry = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'crc_visit'

# Nurse coordinator visit model
class NCVisit(models.Model):
    ncv_id = models.AutoField(primary_key=True)
    infusion = models.FloatField(blank=True, null=True)
    pk_samples = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'nc_visit'


# Data coordinator visit model
class DCVisit(models.Model):
    dcv_id = models.AutoField(primary_key=True)
    infusion = models.FloatField(blank=True, null=True)
    pk_samples = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'dc_visit'


# General visit model
class GeneralVisit(models.Model):
    gv_id = models.AutoField(primary_key=True)
    training = models.FloatField(blank=True, null=True)
    protocol_review = models.FloatField(blank=True, null=True)
    source_document = models.FloatField(blank=True, null=True)
    regulatory = models.FloatField(blank=True, null=True)
    sponsor_meetings = models.FloatField(blank=True, null=True)
    internal_meetings = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'g_visit'
