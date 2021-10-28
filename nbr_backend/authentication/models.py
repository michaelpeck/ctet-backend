from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from django.utils import timezone
import datetime


# Users model (SNAP users)
class UserProfiles(models.Model):
    id = models.IntegerField(primary_key=True, db_column='PERSON_ID')
    network_id = models.CharField(max_length=35, blank=True, null=True, db_column='PERSON_NETWORK_ID')
    employee_id = models.CharField(max_length=9, blank=True, null=True, db_column='PERSON_EMPLOYEE_ID')
    is_employee = models.IntegerField(blank=True, null=True, db_column='PERSON_IS_EMPLOYEE')
    reports_to_1 = models.CharField(max_length=8, blank=True, null=True, db_column='PERSON_REPORTS_TO_1')
    reports_to_2 = models.CharField(max_length=8, blank=True, null=True, db_column='PERSON_REPORTS_TO_2')
    is_active = models.IntegerField(blank=True, null=True, db_column='PERSON_IS_ACTIVE')
    first_name = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_NAME_FIRST')
    mi_name = models.CharField(max_length=8, blank=True, null=True, db_column='PERSON_NAME_INIT')
    last_name = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_NAME_LAST')
    nick_name = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_NAME_NICK')
    start_date = models.DateTimeField(blank=True, null=True, db_column='PERSON_START_DT')
    end_date = models.DateTimeField(blank=True, null=True, db_column='PERSON_END_DT')
    employee_level = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_EMP_LVL')
    employee_type = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_EMP_TYPE')
    job_title = models.CharField(max_length=99, blank=True, null=True, db_column='PERSON_JOB_TITLE')
    site = models.CharField(max_length=42, blank=True, null=True, db_column='PERSON_SITE')
    site_group = models.CharField(max_length=18, blank=True, null=True, db_column='PERSON_SITE_GROUP')
    region = models.CharField(max_length=8, blank=True, null=True, db_column='PERSON_REGION')
    dept_name = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_DEPT_NAME')
    dept_code = models.CharField(max_length=8, blank=True, null=True, db_column='PERSON_DEPT_CODE')
    ph_office_1 = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_PH_OFFICE_1')
    ph_office_2 = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_PH_OFFICE_2')
    ph_cell = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_PH_CELL')
    updated_at = models.DateTimeField(blank=True, null=True, db_column='PERSON_UPDATE_DT')
    created_at = models.DateTimeField(blank=True, null=True, db_column='PERSON_CREATE_DT')
    addr_1 = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_WK_ADDR1')
    addr_2 = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_WK_ADDR2')
    city = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_WK_CITY')
    state = models.CharField(max_length=32, blank=True, null=True, db_column='PERSON_WK_STATE')
    zip = models.CharField(max_length=10, blank=True, null=True, db_column='PERSON_WK_ZIP')
    email_1 = models.CharField(max_length=42, blank=True, null=True, db_column='AD_EMAIL_1')
    email_2 = models.CharField(max_length=42, blank=True, null=True, db_column='AD_EMAIL_2')


    class Meta:
        managed = False
        db_table = 'profiles_nemours'
