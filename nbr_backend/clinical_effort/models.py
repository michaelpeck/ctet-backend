from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from django.utils import timezone
import datetime

## OVERALL
# Clinical trial effort instance model
class CTEffort(models.Model):
    id = models.AutoField(primary_key=True)
    eid = models.CharField(max_length=32, blank=True, null=True)
    user = models.IntegerField(blank=True, null=True)
    protocol_number = models.CharField(max_length=32, blank=True, null=True)
    accounting_number = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    pi = models.CharField(max_length=64, blank=True, null=True)
    estimated_subjects = models.IntegerField(blank=True, null=True, default=0)
    monitor_days = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'effort_models'

## TYPES
# Arm types model
class TrialArmTypes(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trial_arm_types'



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
    type = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'personnel_types'

# Complexity types model
class ComplexityTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    zero = models.CharField(max_length=128, blank=True, null=True)
    one = models.CharField(max_length=128, blank=True, null=True)
    two = models.CharField(max_length=128, blank=True, null=True)
    three = models.CharField(max_length=128, blank=True, null=True)
    three = models.CharField(max_length=128, blank=True, null=True)
    weight = models.FloatField(blank=True, default=0)
    follow_up = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        managed = True
        db_table = 'complexity_types'


## PEOPLE
# Personnel model
class Personnel(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    type = models.ForeignKey('PersonnelTypes',on_delete=models.CASCADE,)
    name = models.CharField(max_length=32, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    year_hours = models.IntegerField(blank=True, null=True, default=2080)
    addl_lump_hours = models.IntegerField(blank=True, null=True, default=0)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'personnel'




## VISITS
# Trial arms model
class TrialArms(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    type = models.ForeignKey('TrialArmTypes',on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    estimated_duration = models.FloatField(blank=True, default=0)
    start_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    end_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trial_arms'
        ordering = ['type']


# Personnel field
class PersonnelFields(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey('Personnel',on_delete=models.CASCADE,)
    arm = models.ForeignKey('TrialArms',on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'personnel_fields'

# Years model
class Years(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)
    name = models.CharField(max_length=32, blank=True, null=True, default = 'Year')

    class Meta:
        managed = True
        db_table = 'years'

# Year value
class YearValues(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.ForeignKey('Years',on_delete=models.CASCADE,)
    arm = models.ForeignKey('TrialArms',on_delete=models.CASCADE,)
    value = models.FloatField(blank=True, default=0)

    class Meta:
        managed = True
        db_table = 'year_values'
        ordering = ['arm__type']

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
        ordering = ['cycle_number', 'visit_number']

# Visit value
class VisitValues(models.Model):
    id = models.AutoField(primary_key=True)
    field = models.ForeignKey('PersonnelFields',on_delete=models.CASCADE,)
    visit = models.ForeignKey('Visits',on_delete=models.CASCADE,)
    value = models.FloatField(blank=True, default=0)

    class Meta:
        managed = True
        db_table = 'visit_values'
        ordering = ['visit__cycle']

## COMPLEXITY
# Complexity model
class Complexity(models.Model):
    id = models.AutoField(primary_key=True)
    instance = models.ForeignKey('CTEffort',on_delete=models.CASCADE,)

    class Meta:
        managed = True
        db_table = 'complexity'


# Complexity value model
class ComplexityValues(models.Model):
    id = models.AutoField(primary_key=True)
    complexity = models.ForeignKey('Complexity',on_delete=models.CASCADE,)
    type = models.ForeignKey('ComplexityTypes',on_delete=models.CASCADE,)
    value = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'complexity_values'


## DEFAULT TABLES
# Personnel Defaults
class PersonnelDefaults(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey('PersonnelTypes',on_delete=models.CASCADE,)
    name = models.CharField(max_length=64, blank=True, null=True)
    text = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'personnel_defaults'
