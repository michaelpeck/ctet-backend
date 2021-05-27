# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from .managers import CustomUserManager

# Clone field function to get fields from AbstractBaseUser
def clone_field(model_class, name, **kwargs):
    name, klass_path, fargs, fkwargs = model_class._meta.get_field(name).deconstruct()
    fkwargs.update(kwargs)
    field_class = import_string(klass_path)
    return field_class(*fargs, **fkwargs)


# User models
# serializers.py, api.py
class User(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    username = clone_field(AbstractUser, 'username', db_column='name')
    password = clone_field(AbstractBaseUser, 'password', db_column='pass')
    mail = models.CharField(max_length=64, blank=True, null=True)
    # mode = models.IntegerField()
    # sort = models.IntegerField(blank=True, null=True)
    # threshold = models.IntegerField(blank=True, null=True)
    # theme = models.CharField(max_length=255)
    signature = models.CharField(max_length=255)
    # signature_format = models.SmallIntegerField()
    # date_joined = clone_field(AbstractUser, 'date_joined', db_column='created')
    # dt_last_login from django.db.models.functions import Now
    # last_login = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='access', default=datetime.datetime.now())
    last_login = models.DateTimeField(auto_now=True)
    # clone_field(AbstractBaseUser, 'last_login', default=timezone.now)
    # models.DateTimeField(auto_now=True)
    #
    # login = models.IntegerField()
    is_active = clone_field(AbstractUser, 'is_active', db_column='status')
    # is_active = models.BooleanField(default=True, db_column='status')
    is_admin = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    # timezone = models.CharField(max_length=8, blank=True, null=True)
    # language = models.CharField(max_length=12)
    # picture = models.CharField(max_length=255)
    # init = models.CharField(max_length=64, blank=True, null=True)
    # data = models.TextField(blank=True, null=True)
    # timezone_name = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # @property
    # def is_superuser(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_superuser
    #
    # @property
    # def is_active(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_active

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin



# Users model (SNAP users)
# serializers.py, api.py
class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    mail = models.CharField(max_length=64, blank=True, null=True)
    # mode = models.IntegerField()
    # sort = models.IntegerField(blank=True, null=True)
    # threshold = models.IntegerField(blank=True, null=True)
    # theme = models.CharField(max_length=255)
    # signature = models.CharField(max_length=255)
    # signature_format = models.SmallIntegerField()
    # date_joined = clone_field(AbstractUser, 'date_joined', db_column='created')
    # dt_last_login from django.db.models.functions import Now
    # last_login = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='access', default=datetime.datetime.now())
    # last_login = clone_field(AbstractBaseUser, 'last_login', default=timezone.now)
    # login = models.IntegerField()
    # is_ative = clone_field(AbstractUser, 'is_active', db_column='status')
    # timezone = models.CharField(max_length=8, blank=True, null=True)
    # language = models.CharField(max_length=12)
    # picture = models.CharField(max_length=255)
    # init = models.CharField(max_length=64, blank=True, null=True)
    # data = models.TextField(blank=True, null=True)
    # timezone_name = models.CharField(max_length=50)
    is_admin = models.BooleanField(default = False)

    class Meta:
        managed = False
        db_table = 'users'

# User Profile Table
# serializers.py, api.py
class RspUserProfile(models.Model):
    profile_id = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    nemours_directory = models.TextField(blank=True, null=True)
    lawson_id = models.TextField(blank=True, null=True)
    degrees_and_credentials = models.TextField(blank=True, null=True)
    departmental_unit = models.TextField(blank=True, null=True)
    research_areas = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    alt_phone = models.CharField(max_length=14, blank=True, null=True)
    cell_phone = models.CharField(max_length=14, blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    alt_email = models.TextField(blank=True, null=True)
    fax = models.CharField(max_length=14, blank=True, null=True)
    site = models.TextField(blank=True, null=True)
    building = models.TextField(blank=True, null=True)
    room = models.TextField(blank=True, null=True)
    biosketch = models.IntegerField(blank=True, null=True)
    cv = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_user_profile'

# Content Type Profile Table
# serializers.py, api.py
class ContentTypeProfile(models.Model):
    vid = models.IntegerField(primary_key=True)
    nid = models.IntegerField()
    field_phone_value = models.CharField(max_length=14, blank=True, null=True)
    field_first_name_value = models.CharField(max_length=20, blank=True, null=True)
    field_last_name_value = models.CharField(max_length=30, blank=True, null=True)
    field_title_value = models.TextField(blank=True, null=True)
    field_education_value = models.TextField(blank=True, null=True)
    field_research_value = models.TextField(blank=True, null=True)
    field_prior_research_value = models.TextField(blank=True, null=True)
    field_era_commons_name_value = models.TextField(blank=True, null=True)
    field_era_commons_name_format = models.PositiveIntegerField(blank=True, null=True)
    field_prior_research_format = models.PositiveIntegerField(blank=True, null=True)
    field_research_format = models.PositiveIntegerField(blank=True, null=True)
    field_education_format = models.PositiveIntegerField(blank=True, null=True)
    field_personal_statement_value = models.TextField(blank=True, null=True)
    field_employment_value = models.TextField(blank=True, null=True)
    field_memberships_value = models.TextField(blank=True, null=True)
    field_activities_value = models.TextField(blank=True, null=True)
    field_positions_misc_value = models.TextField(blank=True, null=True)
    field_publications_misc_value = models.TextField(blank=True, null=True)
    field_research_misc_value = models.TextField(blank=True, null=True)
    field_biosketch_name_value = models.TextField(blank=True, null=True)
    field_employment_format = models.PositiveIntegerField(blank=True, null=True)
    field_activities_format = models.PositiveIntegerField(blank=True, null=True)
    field_positions_misc_format = models.PositiveIntegerField(blank=True, null=True)
    field_publications_misc_format = models.PositiveIntegerField(blank=True, null=True)
    field_research_misc_format = models.PositiveIntegerField(blank=True, null=True)
    field_personal_statement_format = models.PositiveIntegerField(blank=True, null=True)
    field_middle_name_value = models.CharField(max_length=20, blank=True, null=True)
    field_nickname_value = models.CharField(max_length=20, blank=True, null=True)
    field_degree_value = models.TextField(blank=True, null=True)
    field_phone_alt_value = models.CharField(max_length=14, blank=True, null=True)
    field_fax_value = models.CharField(max_length=14, blank=True, null=True)
    field_pager_value = models.CharField(max_length=14, blank=True, null=True)
    field_phone_cell_value = models.CharField(max_length=14, blank=True, null=True)
    field_email_alt_value = models.TextField(blank=True, null=True)
    field_site_value = models.TextField(blank=True, null=True)
    field_building_value = models.TextField(blank=True, null=True)
    field_room_value = models.TextField(blank=True, null=True)
    field_memberships_format = models.PositiveIntegerField(blank=True, null=True)
    field_biosketch_title_value = models.TextField(blank=True, null=True)
    field_biosketch_title_format = models.PositiveIntegerField(blank=True, null=True)
    field_bio_value = models.TextField(blank=True, null=True)
    field_suffix_value = models.TextField(blank=True, null=True)
    field_npi_value = models.CharField(max_length=10, blank=True, null=True)
    field_nemours_directory_value = models.TextField(blank=True, null=True)
    field_profile_biosketch_fid = models.IntegerField(blank=True, null=True)
    field_profile_biosketch_list = models.IntegerField(blank=True, null=True)
    field_profile_biosketch_data = models.TextField(blank=True, null=True)
    field_profile_cv_fid = models.IntegerField(blank=True, null=True)
    field_profile_cv_list = models.IntegerField(blank=True, null=True)
    field_profile_cv_data = models.TextField(blank=True, null=True)
    field_primary_title_value = models.CharField(max_length=80, blank=True, null=True)
    field_title_format = models.PositiveIntegerField(blank=True, null=True)
    field_public_email_value = models.TextField(blank=True, null=True)
    field_orcid_id_value = models.TextField(blank=True, null=True)
    field_cpr_title_value = models.CharField(max_length=60, blank=True, null=True)
    field_lawson_id_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_profile'

# User realname table
# serializers.py
class Realname(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)
    realname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'realname'

# RSP Models
class RspCategory(models.Model):
    rsp_category_id = models.AutoField(primary_key=True)
    rsrch_category = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'rsp_category'


class RspCategoryAffl(models.Model):
    category_affl_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    rsrch_category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_category_affl'

# Committee status map table
# serializers.py, api.py
class RspCommitteeStatusMap(models.Model):
    committe_status_map_id = models.AutoField(primary_key=True)
    status_type_id = models.IntegerField()
    current_status_id = models.IntegerField()
    next_status_id = models.IntegerField(blank=True, null=True)
    final_status_flag = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_committee_status_map'


class RspCoreAffl(models.Model):
    core_affl_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    core_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_core_affl'


class RspCores(models.Model):
    core_id = models.AutoField(primary_key=True)
    core_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'rsp_cores'


class RspDepartment(models.Model):
    department_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'rsp_department'


class RspDepartmentAffl(models.Model):
    department_affl_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    department_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_department_affl'


class RspFundingsource(models.Model):
    fundingsourceid = models.AutoField(db_column='fundingSourceID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=255)
    external = models.IntegerField(blank=True, null=True)
    review = models.IntegerField(blank=True, null=True)
    fed = models.IntegerField(blank=True, null=True)
    drug = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zipcode = models.CharField(max_length=13, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_fundingSource'


class RspFundingsourceAffl(models.Model):
    fundingsource_affl_id = models.AutoField(db_column='fundingSource_affl_id', primary_key=True)  # Field name made lowercase.
    proj_id = models.IntegerField()
    fundingsourceid = models.IntegerField(db_column='fundingSourceID')  # Field name made lowercase.
    fund_src_terms = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'rsp_fundingSource_affl'


class RspIntent(models.Model):
    rsp_id = models.AutoField(primary_key=True)
    rsp_proj_num = models.CharField(unique=True, max_length=16)
    rsp_proj_type = models.CharField(max_length=1)
    rsp_proj_pi = models.IntegerField()
    rsp_proj_title = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_intent'


class RspOrg(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_short_name = models.CharField(max_length=10)
    org_long_name = models.CharField(max_length=155, blank=True, null=True)
    org_address1 = models.CharField(max_length=120, blank=True, null=True)
    org_address2 = models.CharField(max_length=120, blank=True, null=True)
    org_city = models.CharField(max_length=120, blank=True, null=True)
    org_state = models.CharField(max_length=50, blank=True, null=True)
    org_zipcode = models.IntegerField(blank=True, null=True)
    org_type = models.CharField(max_length=9, blank=True, null=True)
    org_active = models.IntegerField(blank=True, null=True)
    org_notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_org'


class RspOrgAffl(models.Model):
    org_affl_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    org_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_org_affl'

# Project table
# serializers.py, api.py
class RspProj(models.Model):
    proj_id = models.AutoField(primary_key=True)
    proj_identifier = models.CharField(max_length=17, blank=True, null=True)
    proj_revision = models.IntegerField(blank=True, null=True)
    proj_draft = models.BooleanField(blank=True, null=True)
    drupal_uid = models.IntegerField(blank=True, null=True)
    vid = models.IntegerField(blank=True, null=True)
    proj_last_name = models.CharField(max_length=255, blank=True, null=True)
    proj_mid_name = models.CharField(max_length=255, blank=True, null=True)
    proj_first_name = models.CharField(max_length=255,blank=True, null=True)
    lawson_id = models.CharField(max_length=5, blank=True, null=True)
    proj_pi_email = models.CharField(max_length=100, blank=True, null=True)
    proj_pi_phone = models.CharField(max_length=20, blank=True, null=True)
    proj_pi_fax = models.CharField(max_length=20, blank=True, null=True)
    proj_pi_title = models.CharField(max_length=512, blank=True, null=True)
    proj_pi_dept = models.CharField(max_length=255, blank=True, null=True)
    proj_coinvestigator = models.TextField(blank=True, null=True)
    proj_title = models.CharField(max_length=500, blank=True, null=True)
    proj_abstract = models.TextField(blank=True, null=True)
    proj_lay_desc = models.TextField(blank=True, null=True)
    proj_why_important = models.TextField(blank=True, null=True)
    proj_budget = models.CharField(max_length=25, blank=True, null=True)
    proj_budget_yr1 = models.CharField(max_length=25, blank=True, null=True)
    proj_deadline = models.DateField(blank=True, null=True)
    proj_start_date = models.DateField(blank=True, null=True)
    proj_end_date = models.DateField(blank=True, null=True)
    proj_ext_collab = models.IntegerField(blank=True, null=True)
    proj_collab_org = models.TextField(blank=True, null=True)
    proj_cat_other = models.CharField(max_length=55, blank=True, null=True)
    proj_fund_nemours = models.IntegerField(blank=True, null=True)
    proj_fund_ext = models.IntegerField(blank=True, null=True)
    proj_acct_unit = models.CharField(max_length=8, blank=True, null=True)
    proj_act_center = models.CharField(max_length=10, blank=True, null=True)
    proj_grant_id = models.CharField(max_length=50, blank=True, null=True)
    proj_fed = models.IntegerField(blank=True, null=True)
    proj_fed_agency = models.CharField(max_length=255, blank=True, null=True)
    proj_fed_pa = models.CharField(max_length=255, blank=True, null=True)
    proj_fund_nonfed = models.CharField(max_length=255, blank=True, null=True)
    proj_fund_nonfed_term = models.IntegerField(blank=True, null=True)
    proj_human = models.IntegerField(blank=True, null=True)
    proj_adult = models.IntegerField(blank=True, null=True)
    proj_pharm_drug = models.IntegerField(blank=True, null=True)
    proj_wolfson = models.IntegerField(blank=True, null=True)
    proj_ion_rad = models.IntegerField(blank=True, null=True)
    proj_animal = models.IntegerField(blank=True, null=True)
    proj_radioact = models.IntegerField(blank=True, null=True)
    proj_cog = models.IntegerField(blank=True, null=True)
    proj_loc = models.CharField(max_length=3, blank=True, null=True)
    proj_biosafety_id = models.CharField(max_length=20, blank=True, null=True)
    proj_itp_id = models.CharField(max_length=20, blank=True, null=True)
    irbnet_id = models.IntegerField(db_column='IRBnet_id', blank=True, null=True)  # Field name made lowercase.
    proj_archive = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    modified_ip = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_proj'

# Project Affiliation Table
# serializers.py, api.py
class RspProjAffl(models.Model):
    affl_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    drupal_uid = models.IntegerField()
    affl_type = models.CharField(max_length=18)
    affl_email = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_proj_affl'

# Comment table
# serializers.py, api.py
class RspProjComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    committee_id = models.IntegerField()
    status_id = models.IntegerField()
    status_map_id = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.IntegerField()
    posted_date = models.CharField(max_length=255, blank=True, null=True)
    modified_date = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_proj_comments'


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     # return '{0}.pdf'.format(instance.file_name)
#     return 'reports/'

# Project file table
# serializers.py, api.py
class RspProjFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    media = models.FileField(upload_to='reports/', null=True, blank=True)
    proj_id = models.IntegerField()
    file_cat = models.IntegerField()
    file_committee = models.IntegerField()
    file_name = models.CharField(max_length=55)
    file_label = models.CharField(max_length=100)
    file_tkn = models.CharField(max_length=100)
    drupal_uid = models.IntegerField()
    file_archive = models.IntegerField(blank=True, null=True)
    file_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rsp_proj_file'

# Files Table
# serializers.py
class Files(models.Model):
    fid = models.AutoField(primary_key=True)
    uid = models.PositiveIntegerField()
    filename = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    filemime = models.CharField(max_length=255)
    filesize = models.PositiveIntegerField()
    status = models.IntegerField()
    timestamp = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'files'

# Project File Category Table
# serializers.py, api.py
class RspProjFileCat(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_desc = models.CharField(max_length=55)
    cat_access = models.CharField(max_length=1)
    cat_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_proj_file_cat'


class RspProjIdentifier(models.Model):
    pid = models.AutoField(primary_key=True)
    lawson_id = models.CharField(max_length=5)
    year = models.IntegerField()
    sequence = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'rsp_proj_identifier'


# Status table
# serializers.py, api.py
class RspProjStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_desc = models.CharField(max_length=55)

    class Meta:
        managed = False
        db_table = 'rsp_proj_status'

# Project status log table
# serializers.py, api.py
class RspProjStatusLog(models.Model):
    status_map_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    status_type_id = models.IntegerField()
    status_id = models.IntegerField()
    status_current = models.IntegerField()
    status_comment = models.CharField(max_length=255, blank=True, null=True)
    file_id = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    modified_date = models.CharField(max_length=255, blank=True, null=True)
    status_change_date = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_proj_status_log'


class RspProjTask(models.Model):
    task_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    drupal_uid = models.IntegerField()
    task_desc = models.CharField(max_length=55)
    task_status = models.CharField(max_length=55)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rsp_proj_task'

# Report Email List Table
# serializers.py, api.py
class RspReportEmailList(models.Model):
    elid = models.AutoField(primary_key=True)
    uid = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'rsp_report_email_list'

class RspRequireApproval(models.Model):
    req_approval_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    status_type_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_require_approval'

# Roles Table
# serializers.py, api.py
class RspRoles(models.Model):
    rsp_role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    role_abbrev = models.CharField(max_length=5)
    committee = models.CharField(max_length=100, blank=True, null=True)
    status_type_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_roles'

# Project status type table
# serializers.py
class RspStatusType(models.Model):
    status_type_id = models.AutoField(primary_key=True)
    status_type_name = models.CharField(max_length=100)
    status_display = models.IntegerField()
    status_order = models.IntegerField()
    status_full_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'rsp_status_type'

# User Role Table
# serializers.py, api.py
class RspUserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    rsp_role_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_user_role'


class RspWorksite(models.Model):
    worksite_id = models.AutoField(primary_key=True)
    building = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    org_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_worksite'


class RspWorksiteAffl(models.Model):
    worksite_affl_id = models.AutoField(primary_key=True)
    proj_id = models.IntegerField()
    worksite_id = models.IntegerField()
    primary = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rsp_worksite_affl'

# Node Table
# serializers.py, api.py
class Node(models.Model):
    nid = models.AutoField(primary_key=True)
    vid = models.PositiveIntegerField(unique=True)
    type = models.CharField(max_length=32)
    language = models.CharField(max_length=12)
    title = models.CharField(max_length=255)
    uid = models.IntegerField()
    status = models.IntegerField()
    created = models.IntegerField()
    changed = models.IntegerField()
    comment = models.IntegerField()
    promote = models.IntegerField()
    moderate = models.IntegerField()
    sticky = models.IntegerField()
    tnid = models.PositiveIntegerField()
    translate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'node'

class UsersRoles(models.Model):
    uid = models.PositiveIntegerField(primary_key=True)
    rid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'users_roles'
        unique_together = (('uid', 'rid'),)



class Actions(models.Model):
    aid = models.CharField(primary_key=True, max_length=255)
    type = models.CharField(max_length=32)
    callback = models.CharField(max_length=255)
    parameters = models.TextField()
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'actions'


class ActionsAid(models.Model):
    aid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'actions_aid'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Authmap(models.Model):
    aid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    authname = models.CharField(unique=True, max_length=128)
    module = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'authmap'


class AuthorTaxonomyTermLink(models.Model):
    tid = models.PositiveIntegerField()
    uid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'author_taxonomy_term_link'


class BackreferenceFieldSymmetry(models.Model):
    field_left = models.CharField(primary_key=True, max_length=32)
    field_right = models.CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'backreference_field_symmetry'


class Batch(models.Model):
    bid = models.AutoField(primary_key=True)
    token = models.CharField(max_length=64)
    timestamp = models.IntegerField()
    batch = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch'


class Biblio(models.Model):
    nid = models.IntegerField()
    vid = models.IntegerField(primary_key=True)
    biblio_type = models.IntegerField()
    biblio_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_other_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_secondary_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_tertiary_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_edition = models.CharField(max_length=255, blank=True, null=True)
    biblio_publisher = models.CharField(max_length=255, blank=True, null=True)
    biblio_place_published = models.CharField(max_length=255, blank=True, null=True)
    biblio_year = models.IntegerField()
    biblio_volume = models.CharField(max_length=128, blank=True, null=True)
    biblio_pages = models.CharField(max_length=128, blank=True, null=True)
    biblio_date = models.CharField(max_length=16, blank=True, null=True)
    biblio_isbn = models.CharField(max_length=128, blank=True, null=True)
    biblio_lang = models.CharField(max_length=24, blank=True, null=True)
    biblio_abst_e = models.TextField(blank=True, null=True)
    biblio_abst_f = models.TextField(blank=True, null=True)
    biblio_full_text = models.IntegerField(blank=True, null=True)
    biblio_url = models.CharField(max_length=255, blank=True, null=True)
    biblio_issue = models.CharField(max_length=128, blank=True, null=True)
    biblio_type_of_work = models.CharField(max_length=128, blank=True, null=True)
    biblio_accession_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_call_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_notes = models.TextField(blank=True, null=True)
    biblio_custom1 = models.TextField(blank=True, null=True)
    biblio_custom2 = models.TextField(blank=True, null=True)
    biblio_custom3 = models.TextField(blank=True, null=True)
    biblio_custom4 = models.TextField(blank=True, null=True)
    biblio_custom5 = models.TextField(blank=True, null=True)
    biblio_custom6 = models.TextField(blank=True, null=True)
    biblio_custom7 = models.TextField(blank=True, null=True)
    biblio_research_notes = models.TextField(blank=True, null=True)
    biblio_number_of_volumes = models.CharField(max_length=128, blank=True, null=True)
    biblio_short_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_alternate_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_original_publication = models.CharField(max_length=255, blank=True, null=True)
    biblio_reprint_edition = models.CharField(max_length=255, blank=True, null=True)
    biblio_translated_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_section = models.CharField(max_length=128, blank=True, null=True)
    biblio_citekey = models.CharField(max_length=255, blank=True, null=True)
    biblio_coins = models.TextField(blank=True, null=True)
    biblio_doi = models.CharField(max_length=255, blank=True, null=True)
    biblio_issn = models.CharField(max_length=128, blank=True, null=True)
    biblio_auth_address = models.TextField(blank=True, null=True)
    biblio_remote_db_name = models.CharField(max_length=255, blank=True, null=True)
    biblio_remote_db_provider = models.CharField(max_length=255, blank=True, null=True)
    biblio_label = models.CharField(max_length=255, blank=True, null=True)
    biblio_access_date = models.CharField(max_length=255, blank=True, null=True)
    biblio_refereed = models.CharField(max_length=20, blank=True, null=True)
    biblio_md5 = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio'


class BiblioAbbrev(models.Model):
    abbrev = models.CharField(max_length=128)
    full = models.TextField()

    class Meta:
        managed = False
        db_table = 'biblio_abbrev'


class BiblioCollection(models.Model):
    cid = models.PositiveIntegerField(primary_key=True)
    vid = models.PositiveIntegerField()
    pid = models.PositiveIntegerField()
    nid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_collection'
        unique_together = (('cid', 'vid'),)


class BiblioCollectionType(models.Model):
    cid = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'biblio_collection_type'


class BiblioContributor(models.Model):
    nid = models.PositiveIntegerField()
    vid = models.PositiveIntegerField(primary_key=True)
    cid = models.PositiveIntegerField()
    auth_type = models.PositiveIntegerField()
    auth_category = models.PositiveIntegerField()
    rank = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_contributor'
        unique_together = (('vid', 'cid', 'auth_type', 'rank'),)


class BiblioContributorData(models.Model):
    cid = models.AutoField(primary_key=True)
    aka = models.PositiveIntegerField()
    drupal_uid = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=128, blank=True, null=True)
    prefix = models.CharField(max_length=128, blank=True, null=True)
    suffix = models.CharField(max_length=128, blank=True, null=True)
    initials = models.CharField(max_length=10, blank=True, null=True)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    md5 = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_contributor_data'
        unique_together = (('cid', 'aka'),)


class BiblioContributorType(models.Model):
    auth_category = models.PositiveIntegerField(primary_key=True)
    biblio_type = models.PositiveIntegerField()
    auth_type = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_contributor_type'
        unique_together = (('auth_category', 'biblio_type', 'auth_type'),)


class BiblioContributorTypeData(models.Model):
    auth_type = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    hint = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_contributor_type_data'


class BiblioCrawlerCache(models.Model):
    biblio_type = models.IntegerField()
    biblio_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_other_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_secondary_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_tertiary_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_edition = models.CharField(max_length=255, blank=True, null=True)
    biblio_publisher = models.CharField(max_length=255, blank=True, null=True)
    biblio_place_published = models.CharField(max_length=255, blank=True, null=True)
    biblio_year = models.IntegerField()
    biblio_volume = models.CharField(max_length=128, blank=True, null=True)
    biblio_pages = models.CharField(max_length=128, blank=True, null=True)
    biblio_date = models.CharField(max_length=16, blank=True, null=True)
    biblio_isbn = models.CharField(max_length=128, blank=True, null=True)
    biblio_lang = models.CharField(max_length=24, blank=True, null=True)
    biblio_abst_e = models.TextField(blank=True, null=True)
    biblio_abst_f = models.TextField(blank=True, null=True)
    biblio_full_text = models.IntegerField(blank=True, null=True)
    biblio_url = models.CharField(max_length=255, blank=True, null=True)
    biblio_issue = models.CharField(max_length=128, blank=True, null=True)
    biblio_type_of_work = models.CharField(max_length=128, blank=True, null=True)
    biblio_accession_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_call_number = models.CharField(max_length=128, blank=True, null=True)
    biblio_notes = models.TextField(blank=True, null=True)
    biblio_custom1 = models.TextField(blank=True, null=True)
    biblio_custom2 = models.TextField(blank=True, null=True)
    biblio_custom3 = models.TextField(blank=True, null=True)
    biblio_custom4 = models.TextField(blank=True, null=True)
    biblio_custom5 = models.TextField(blank=True, null=True)
    biblio_custom6 = models.TextField(blank=True, null=True)
    biblio_custom7 = models.TextField(blank=True, null=True)
    biblio_research_notes = models.TextField(blank=True, null=True)
    biblio_number_of_volumes = models.CharField(max_length=128, blank=True, null=True)
    biblio_short_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_alternate_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_original_publication = models.CharField(max_length=255, blank=True, null=True)
    biblio_reprint_edition = models.CharField(max_length=255, blank=True, null=True)
    biblio_translated_title = models.CharField(max_length=255, blank=True, null=True)
    biblio_section = models.CharField(max_length=128, blank=True, null=True)
    biblio_citekey = models.CharField(max_length=255, blank=True, null=True)
    biblio_coins = models.TextField(blank=True, null=True)
    biblio_doi = models.CharField(max_length=255, blank=True, null=True)
    biblio_issn = models.CharField(max_length=128, blank=True, null=True)
    biblio_auth_address = models.TextField(blank=True, null=True)
    biblio_remote_db_name = models.CharField(max_length=255, blank=True, null=True)
    biblio_remote_db_provider = models.CharField(max_length=255, blank=True, null=True)
    biblio_label = models.CharField(max_length=255, blank=True, null=True)
    biblio_access_date = models.CharField(max_length=255, blank=True, null=True)
    biblio_refereed = models.CharField(max_length=20, blank=True, null=True)
    biblio_md5 = models.CharField(max_length=32, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    biblio_contributors = models.TextField(blank=True, null=True)
    title = models.TextField()
    nid = models.IntegerField(blank=True, null=True)
    crawler_view_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_crawler_cache'


class BiblioCrawlerCacheFetch(models.Model):
    crawler_cache_id = models.IntegerField()
    crawler_fetch_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_crawler_cache_fetch'


class BiblioCrawlerFetch(models.Model):
    crawler_search_id = models.IntegerField()
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_crawler_fetch'


class BiblioCrawlerSearch(models.Model):
    drupal_uid = models.PositiveIntegerField(blank=True, null=True)
    match_terms = models.TextField(blank=True, null=True)
    exclude_terms = models.TextField(blank=True, null=True)
    min_year = models.IntegerField(blank=True, null=True)
    max_year = models.IntegerField(blank=True, null=True)
    nrec = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_crawler_search'


class BiblioCrawlerSearchSource(models.Model):
    crawler_search_id = models.IntegerField(blank=True, null=True)
    crawler_source_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_crawler_search_source'


class BiblioCrawlerSource(models.Model):
    name = models.TextField(blank=True, null=True)
    short_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_crawler_source'


class BiblioDuplicates(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    did = models.PositiveIntegerField()
    type = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_duplicates'
        unique_together = (('vid', 'did'),)


class BiblioFieldType(models.Model):
    tid = models.PositiveIntegerField(primary_key=True)
    fid = models.PositiveIntegerField()
    ftdid = models.PositiveIntegerField()
    cust_tdid = models.PositiveIntegerField()
    common = models.PositiveIntegerField()
    autocomplete = models.PositiveIntegerField()
    required = models.PositiveIntegerField()
    weight = models.IntegerField()
    visible = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_field_type'
        unique_together = (('tid', 'fid'),)


class BiblioFieldTypeData(models.Model):
    ftdid = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    hint = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_field_type_data'


class BiblioFields(models.Model):
    fid = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    size = models.PositiveIntegerField()
    maxsize = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_fields'


class BiblioImportCache(models.Model):
    session_id = models.CharField(max_length=45)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_import_cache'


class BiblioKeyword(models.Model):
    kid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    vid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_keyword'
        unique_together = (('kid', 'vid'),)


class BiblioKeywordData(models.Model):
    kid = models.AutoField(primary_key=True)
    word = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'biblio_keyword_data'


class BiblioPubmed(models.Model):
    biblio_pubmed_id = models.IntegerField()
    nid = models.IntegerField(primary_key=True)
    biblio_pubmed_md5 = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'biblio_pubmed'


class BiblioTypeMaps(models.Model):
    format = models.CharField(primary_key=True, max_length=128)
    type_map = models.TextField(blank=True, null=True)
    type_names = models.TextField(blank=True, null=True)
    field_map = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biblio_type_maps'


class BiblioTypes(models.Model):
    tid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, null=True)
    weight = models.IntegerField()
    visible = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'biblio_types'


class Blocks(models.Model):
    bid = models.AutoField(primary_key=True)
    module = models.CharField(max_length=64)
    delta = models.CharField(max_length=32)
    theme = models.CharField(max_length=64)
    status = models.IntegerField()
    weight = models.IntegerField()
    region = models.CharField(max_length=64)
    custom = models.IntegerField()
    throttle = models.IntegerField()
    visibility = models.IntegerField()
    pages = models.TextField()
    title = models.CharField(max_length=64)
    cache = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'blocks'
        unique_together = (('theme', 'module', 'delta'),)


class BlocksRoles(models.Model):
    module = models.CharField(primary_key=True, max_length=64)
    delta = models.CharField(max_length=32)
    rid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'blocks_roles'
        unique_together = (('module', 'delta', 'rid'),)


class Book(models.Model):
    mlid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField(unique=True)
    bid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'book'


class Boxes(models.Model):
    bid = models.AutoField(primary_key=True)
    body = models.TextField(blank=True, null=True)
    info = models.CharField(unique=True, max_length=128)
    format = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'boxes'


class CkeditorRole(models.Model):
    name = models.CharField(primary_key=True, max_length=128)
    rid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ckeditor_role'
        unique_together = (('name', 'rid'),)


class CkeditorSettings(models.Model):
    name = models.CharField(primary_key=True, max_length=128)
    settings = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ckeditor_settings'


class Comments(models.Model):
    cid = models.AutoField(primary_key=True)
    pid = models.IntegerField()
    nid = models.IntegerField()
    uid = models.IntegerField()
    subject = models.CharField(max_length=64)
    comment = models.TextField()
    hostname = models.CharField(max_length=128)
    timestamp = models.IntegerField()
    status = models.PositiveIntegerField()
    format = models.SmallIntegerField()
    thread = models.CharField(max_length=255)
    name = models.CharField(max_length=60, blank=True, null=True)
    mail = models.CharField(max_length=64, blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class CommunityTags(models.Model):
    tid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    uid = models.PositiveIntegerField()
    date = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'community_tags'
        unique_together = (('tid', 'uid', 'nid'),)


class Contact(models.Model):
    cid = models.AutoField(primary_key=True)
    category = models.CharField(unique=True, max_length=255)
    recipients = models.TextField()
    reply = models.TextField()
    weight = models.IntegerField()
    selected = models.IntegerField()
    page_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'


class ContentFieldCenter(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_center_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_center'
        unique_together = (('vid', 'delta'),)


class ContentFieldCenterMember(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_center_member_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_center_member'
        unique_together = (('vid', 'delta'),)


class ContentFieldCommittee(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_committee_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_committee'
        unique_together = (('vid', 'delta'),)


class ContentFieldCommitteeEditors(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_committee_editors_uid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_committee_editors'
        unique_together = (('vid', 'delta'),)


class ContentFieldCommitteeMember(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_committee_member_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_committee_member'
        unique_together = (('vid', 'delta'),)


class ContentFieldCoreDept(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_core_dept_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_core_dept'
        unique_together = (('vid', 'delta'),)


class ContentFieldCoreDirectorNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_core_director_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_core_director_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldCoreEditor(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_core_editor_uid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_core_editor'
        unique_together = (('vid', 'delta'),)


class ContentFieldCoreLab(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_core_lab_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_core_lab'
        unique_together = (('vid', 'delta'),)


class ContentFieldCoreLabMember(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_core_lab_member_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_core_lab_member'
        unique_together = (('vid', 'delta'),)


class ContentFieldCoreProjects(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_core_projects_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_core_projects'
        unique_together = (('vid', 'delta'),)


class ContentFieldCoreStaff(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_core_staff_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_core_staff'
        unique_together = (('vid', 'delta'),)


class ContentFieldCorelabEditor(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_corelab_editor_uid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_corelab_editor'
        unique_together = (('vid', 'delta'),)


class ContentFieldCorelabProjects(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_corelab_projects_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_corelab_projects'
        unique_together = (('vid', 'delta'),)


class ContentFieldDepartment(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_department_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_department'
        unique_together = (('vid', 'delta'),)


class ContentFieldDeptCores(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_dept_cores_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_dept_cores'
        unique_together = (('vid', 'delta'),)


class ContentFieldDeptDirectors(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_dept_directors_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_dept_directors'
        unique_together = (('vid', 'delta'),)


class ContentFieldDeptEditor(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_dept_editor_uid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_dept_editor'
        unique_together = (('vid', 'delta'),)


class ContentFieldDeptProjects(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_dept_projects_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_dept_projects'
        unique_together = (('vid', 'delta'),)


class ContentFieldEditors(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_editors_uid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_editors'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduCity(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_city_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_city'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduCountry(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_country_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_country'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduDegree(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_degree_value = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_degree'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduField(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_field_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_field'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduInstitution(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_institution_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_institution'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduMonth(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_month_value = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_month'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduState(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_state_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_state'
        unique_together = (('vid', 'delta'),)


class ContentFieldEduYear(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_edu_year_value = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_edu_year'
        unique_together = (('vid', 'delta'),)


class ContentFieldGrantCoPiNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_grant_co_pi_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_grant_co_pi_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldGrantKeyNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_grant_key_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_grant_key_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldGrantNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_grant_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_grant_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldGrantPiNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_grant_pi_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_grant_pi_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldGrantProjects(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_grant_projects_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_grant_projects'
        unique_together = (('vid', 'delta'),)


class ContentFieldGrantRole(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_grant_role_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_grant_role'
        unique_together = (('vid', 'delta'),)


class ContentFieldInternalOnly(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_internal_only_value = models.TextField(blank=True, null=True)
    field_internal_only_format = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_internal_only'


class ContentFieldLabHeadNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_lab_head_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_lab_head_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldMembersCommittee(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_members_committee_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_members_committee'
        unique_together = (('vid', 'delta'),)


class ContentFieldOffice(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_office_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_office'
        unique_together = (('vid', 'delta'),)


class ContentFieldOfficeMember(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_office_member_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_office_member'
        unique_together = (('vid', 'delta'),)


class ContentFieldProfileCores(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_profile_cores_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_profile_cores'
        unique_together = (('vid', 'delta'),)


class ContentFieldProfileEditor(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_profile_editor_uid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_profile_editor'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjDesc(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_proj_desc_value = models.TextField(blank=True, null=True)
    field_proj_desc_format = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_proj_desc'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjPi(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_proj_pi_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_proj_pi'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjRole(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_proj_role_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_proj_role'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjTitle(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_proj_title_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_proj_title'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectCoinvestNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_coinvest_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_coinvest_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectCore(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_core_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_core'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectCoreLab(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_core_lab_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_core_lab'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectDept(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_dept_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_dept'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectEditor(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_editor_uid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_editor'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectGrant(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_grant_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_grant'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectRaNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_ra_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_ra_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldProjectStudycoordNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_project_studycoord_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_project_studycoord_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldResearchAreas(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_research_areas_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_research_areas'
        unique_together = (('vid', 'delta'),)


class ContentFieldStaffCoreLab(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_staff_core_lab_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_staff_core_lab'
        unique_together = (('vid', 'delta'),)


class ContentFieldStaffNode(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_staff_node_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_staff_node'
        unique_together = (('vid', 'delta'),)


class ContentFieldStaffOffice(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    delta = models.PositiveIntegerField()
    field_staff_office_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_field_staff_office'
        unique_together = (('vid', 'delta'),)


class ContentGroup(models.Model):
    group_type = models.CharField(max_length=32)
    type_name = models.CharField(primary_key=True, max_length=32)
    group_name = models.CharField(max_length=32)
    label = models.CharField(max_length=255)
    settings = models.TextField()
    weight = models.IntegerField()
    parent = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_group'
        unique_together = (('type_name', 'group_name'),)


class ContentGroupFields(models.Model):
    type_name = models.CharField(primary_key=True, max_length=32)
    group_name = models.CharField(max_length=32)
    field_name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'content_group_fields'
        unique_together = (('type_name', 'group_name', 'field_name'),)


class ContentNodeField(models.Model):
    field_name = models.CharField(primary_key=True, max_length=32)
    type = models.CharField(max_length=127)
    global_settings = models.TextField()
    required = models.IntegerField()
    multiple = models.IntegerField()
    db_storage = models.IntegerField()
    module = models.CharField(max_length=127)
    db_columns = models.TextField()
    active = models.IntegerField()
    locked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'content_node_field'


class ContentNodeFieldInstance(models.Model):
    field_name = models.CharField(primary_key=True, max_length=32)
    type_name = models.CharField(max_length=32)
    weight = models.IntegerField()
    label = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=32)
    widget_settings = models.TextField()
    display_settings = models.TextField()
    description = models.TextField()
    widget_module = models.CharField(max_length=127)
    widget_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'content_node_field_instance'
        unique_together = (('field_name', 'type_name'),)


class ContentTypeCenter(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'content_type_center'


class ContentTypeCenterSub(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_master_dept_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_center_sub'


class ContentTypeCommiteesSub(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_master_committee_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_commitees_sub'


class ContentTypeCommittee(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'content_type_committee'


class ContentTypeCore(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'content_type_core'


class ContentTypeCoreSub(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_master_core_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_core_sub'


class ContentTypeGrant(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_grant_number_value = models.TextField(blank=True, null=True)
    field_grant_agency_value = models.TextField(blank=True, null=True)
    field_brief_summary_value = models.TextField(blank=True, null=True)
    field_grant_abstract_value = models.TextField(blank=True, null=True)
    field_brief_summary_format = models.PositiveIntegerField(blank=True, null=True)
    field_grant_abstract_format = models.PositiveIntegerField(blank=True, null=True)
    field_grant_funding_value = models.TextField(blank=True, null=True)
    field_grant_start_value = models.TextField(blank=True, null=True)
    field_grant_end_value = models.TextField(blank=True, null=True)
    field_grant_award_value = models.IntegerField(blank=True, null=True)
    field_grant_funding_other_value = models.TextField(blank=True, null=True)
    field_grant_status_value = models.TextField(blank=True, null=True)
    field_grant_pi_other_value = models.TextField(blank=True, null=True)
    field_grant_pi_other_format = models.PositiveIntegerField(blank=True, null=True)
    field_grant_co_pi_other_value = models.TextField(blank=True, null=True)
    field_grant_co_pi_other_format = models.PositiveIntegerField(blank=True, null=True)
    field_grant_key_more_value = models.TextField(blank=True, null=True)
    field_grant_key_more_format = models.PositiveIntegerField(blank=True, null=True)
    field_grant_title_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_grant'


class ContentTypeLab(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'content_type_lab'


class ContentTypeLabSub(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_master_corelab_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_lab_sub'


class ContentTypeOffice(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_unit_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_office'


class ContentTypeOfficesub(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_officemaster_nid = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_officesub'


class ContentTypePage(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'content_type_page'





class ContentTypeProject(models.Model):
    vid = models.PositiveIntegerField(primary_key=True)
    nid = models.PositiveIntegerField()
    field_project_staff_value = models.TextField(blank=True, null=True)
    field_project_staff_format = models.PositiveIntegerField(blank=True, null=True)
    field_project_descr_value = models.TextField(blank=True, null=True)
    field_project_descr_format = models.PositiveIntegerField(blank=True, null=True)
    field_other_funding_value = models.TextField(blank=True, null=True)
    field_project_pi_node_nid = models.PositiveIntegerField(blank=True, null=True)
    field_project_coinvest_other_value = models.TextField(blank=True, null=True)
    field_project_studycoord_other_value = models.TextField(blank=True, null=True)
    field_project_ra_other_value = models.TextField(blank=True, null=True)
    field_project_coinvest_other_format = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_type_project'


class CtoolsCssCache(models.Model):
    cid = models.CharField(primary_key=True, max_length=128)
    filename = models.CharField(max_length=255, blank=True, null=True)
    css = models.TextField(blank=True, null=True)
    filter = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ctools_css_cache'


class CtoolsObjectCache(models.Model):
    sid = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=128)
    obj = models.CharField(max_length=32)
    updated = models.PositiveIntegerField()
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ctools_object_cache'
        unique_together = (('sid', 'obj', 'name'),)


class DateFormatLocale(models.Model):
    format = models.CharField(max_length=100)
    type = models.CharField(primary_key=True, max_length=200)
    language = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'date_format_locale'
        unique_together = (('type', 'language'),)


class DateFormatTypes(models.Model):
    type = models.CharField(primary_key=True, max_length=200)
    title = models.CharField(max_length=255)
    locked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'date_format_types'


class DateFormats(models.Model):
    dfid = models.AutoField(primary_key=True)
    format = models.CharField(max_length=100)
    type = models.CharField(max_length=200)
    locked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'date_formats'
        unique_together = (('format', 'type'),)


class DevelQueries(models.Model):
    qid = models.AutoField(primary_key=True)
    function = models.CharField(max_length=255)
    query = models.TextField()
    hash = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'devel_queries'


class DevelTimes(models.Model):
    tid = models.AutoField(primary_key=True)
    qid = models.IntegerField()
    time = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devel_times'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FilterFormats(models.Model):
    format = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    roles = models.CharField(max_length=255)
    cache = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'filter_formats'


class Filters(models.Model):
    fid = models.AutoField(primary_key=True)
    format = models.IntegerField()
    module = models.CharField(max_length=64)
    delta = models.IntegerField()
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'filters'
        unique_together = (('format', 'module', 'delta'),)


class Flood(models.Model):
    fid = models.AutoField(primary_key=True)
    event = models.CharField(max_length=64)
    hostname = models.CharField(max_length=128)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'flood'


class History(models.Model):
    uid = models.IntegerField(primary_key=True)
    nid = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'history'
        unique_together = (('uid', 'nid'),)


class HoneypotUser(models.Model):
    uid = models.PositiveIntegerField()
    timestamp = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'honeypot_user'


class ImagecacheAction(models.Model):
    actionid = models.AutoField(primary_key=True)
    presetid = models.PositiveIntegerField()
    weight = models.IntegerField()
    module = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'imagecache_action'


class ImagecachePreset(models.Model):
    presetid = models.AutoField(primary_key=True)
    presetname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'imagecache_preset'


class NodeAccess(models.Model):
    nid = models.PositiveIntegerField(primary_key=True)
    gid = models.PositiveIntegerField()
    realm = models.CharField(max_length=255)
    grant_view = models.PositiveIntegerField()
    grant_update = models.PositiveIntegerField()
    grant_delete = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'node_access'
        unique_together = (('nid', 'gid', 'realm'),)


class NodeCommentStatistics(models.Model):
    nid = models.PositiveIntegerField(primary_key=True)
    last_comment_timestamp = models.IntegerField()
    last_comment_name = models.CharField(max_length=60, blank=True, null=True)
    last_comment_uid = models.IntegerField()
    comment_count = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'node_comment_statistics'


class NodeConvertTemplates(models.Model):
    nctid = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    source_type = models.TextField(blank=True, null=True)
    destination_type = models.TextField()
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_convert_templates'


class NodeCounter(models.Model):
    nid = models.IntegerField(primary_key=True)
    totalcount = models.BigIntegerField()
    daycount = models.PositiveIntegerField()
    timestamp = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'node_counter'


class NodeImportStatus(models.Model):
    taskid = models.PositiveIntegerField(primary_key=True)
    file_offset = models.PositiveIntegerField()
    errors = models.TextField()
    objid = models.PositiveIntegerField()
    status = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'node_import_status'
        unique_together = (('taskid', 'file_offset'),)


class NodeImportTasks(models.Model):
    taskid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    uid = models.PositiveIntegerField()
    created = models.PositiveIntegerField()
    changed = models.PositiveIntegerField()
    fid = models.PositiveIntegerField()
    has_headers = models.PositiveIntegerField()
    file_options = models.TextField()
    headers = models.TextField()
    type = models.CharField(max_length=64)
    map = models.TextField()
    defaults = models.TextField()
    options = models.TextField()
    file_offset = models.PositiveIntegerField()
    row_done = models.PositiveIntegerField()
    row_error = models.PositiveIntegerField()
    status = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'node_import_tasks'


class NodeRevisions(models.Model):
    nid = models.PositiveIntegerField()
    vid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    teaser = models.TextField()
    log = models.TextField()
    timestamp = models.IntegerField()
    format = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'node_revisions'


class NodeType(models.Model):
    type = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    description = models.TextField()
    help = models.TextField()
    has_title = models.PositiveIntegerField()
    title_label = models.CharField(max_length=255)
    has_body = models.PositiveIntegerField()
    body_label = models.CharField(max_length=255)
    min_word_count = models.PositiveSmallIntegerField()
    custom = models.IntegerField()
    modified = models.IntegerField()
    locked = models.IntegerField()
    orig_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'node_type'


class PageManagerWeights(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    weight = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page_manager_weights'


class Permission(models.Model):
    pid = models.AutoField(primary_key=True)
    rid = models.PositiveIntegerField()
    perm = models.TextField(blank=True, null=True)
    tid = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'permission'


class ProfileFields(models.Model):
    fid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(unique=True, max_length=128)
    explanation = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    page = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=128, blank=True, null=True)
    weight = models.IntegerField()
    required = models.IntegerField()
    register = models.IntegerField()
    visibility = models.IntegerField()
    autocomplete = models.IntegerField()
    options = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile_fields'


class ProfileValues(models.Model):
    fid = models.PositiveIntegerField()
    uid = models.PositiveIntegerField(primary_key=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile_values'
        unique_together = (('uid', 'fid'),)




class Role(models.Model):
    rid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'role'


class SearchDataset(models.Model):
    sid = models.PositiveIntegerField()
    type = models.CharField(max_length=16, blank=True, null=True)
    data = models.TextField()
    reindex = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'search_dataset'
        unique_together = (('sid', 'type'),)


class SearchIndex(models.Model):
    word = models.CharField(max_length=50)
    sid = models.PositiveIntegerField()
    type = models.CharField(max_length=16, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_index'
        unique_together = (('word', 'sid', 'type'),)


class SearchNodeLinks(models.Model):
    sid = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=16)
    nid = models.PositiveIntegerField()
    caption = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_node_links'
        unique_together = (('sid', 'type', 'nid'),)


class SearchTotal(models.Model):
    word = models.CharField(primary_key=True, max_length=50)
    count = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_total'


class Semaphore(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    value = models.CharField(max_length=255)
    expire = models.FloatField()

    class Meta:
        managed = False
        db_table = 'semaphore'


class ServicesProject(models.Model):
    modified_date = models.DateTimeField()
    proj_first_name = models.CharField(max_length=100)
    proj_id = models.IntegerField(blank=True, null=True)
    proj_identifier = models.CharField(max_length=100)
    proj_last_name = models.CharField(max_length=100)
    proj_title = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'services_project'


class Sessions(models.Model):
    uid = models.PositiveIntegerField()
    sid = models.CharField(primary_key=True, max_length=64)
    hostname = models.CharField(max_length=128)
    timestamp = models.IntegerField()
    cache = models.IntegerField()
    session = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class System(models.Model):
    filename = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    status = models.IntegerField()
    throttle = models.IntegerField()
    bootstrap = models.IntegerField()
    schema_version = models.SmallIntegerField()
    weight = models.IntegerField()
    info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system'


class TermData(models.Model):
    tid = models.AutoField(primary_key=True)
    vid = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'term_data'


class TermHierarchy(models.Model):
    tid = models.PositiveIntegerField(primary_key=True)
    parent = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'term_hierarchy'
        unique_together = (('tid', 'parent'),)


class TermNode(models.Model):
    nid = models.PositiveIntegerField()
    vid = models.PositiveIntegerField()
    tid = models.PositiveIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'term_node'
        unique_together = (('tid', 'vid'),)


class TermRelation(models.Model):
    trid = models.AutoField(primary_key=True)
    tid1 = models.PositiveIntegerField()
    tid2 = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'term_relation'
        unique_together = (('tid1', 'tid2'),)


class TermSynonym(models.Model):
    tsid = models.AutoField(primary_key=True)
    tid = models.PositiveIntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'term_synonym'


class Upload(models.Model):
    fid = models.PositiveIntegerField()
    nid = models.PositiveIntegerField()
    vid = models.PositiveIntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    list = models.PositiveIntegerField()
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'upload'
        unique_together = (('vid', 'fid'),)


class UrlAlias(models.Model):
    pid = models.AutoField(primary_key=True)
    src = models.CharField(max_length=128)
    dst = models.CharField(max_length=128)
    language = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'url_alias'
        unique_together = (('dst', 'language', 'pid'),)


class UserImport(models.Model):
    import_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    filename = models.CharField(max_length=50)
    oldfilename = models.CharField(max_length=50)
    filepath = models.TextField()
    started = models.IntegerField()
    pointer = models.IntegerField()
    processed = models.IntegerField()
    valid = models.IntegerField()
    field_match = models.TextField()
    roles = models.TextField()
    options = models.TextField()
    setting = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'user_import'


class UserImportErrors(models.Model):
    import_id = models.IntegerField()
    data = models.TextField()
    errors = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_import_errors'


class Variable(models.Model):
    name = models.CharField(primary_key=True, max_length=128)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'variable'


class VivoKeywordExclude(models.Model):
    kid = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'vivo_keyword_exclude'


class VivoProfileMap(models.Model):
    uid = models.IntegerField(primary_key=True)
    snap_uid = models.IntegerField(blank=True, null=True)
    accel_uid = models.IntegerField(blank=True, null=True)
    vivo_include = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vivo_profile_map'


class Vocabulary(models.Model):
    vid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    help = models.CharField(max_length=255)
    relations = models.PositiveIntegerField()
    hierarchy = models.PositiveIntegerField()
    multiple = models.PositiveIntegerField()
    required = models.PositiveIntegerField()
    tags = models.PositiveIntegerField()
    module = models.CharField(max_length=255)
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vocabulary'


class VocabularyNodeTypes(models.Model):
    vid = models.PositiveIntegerField()
    type = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'vocabulary_node_types'
        unique_together = (('type', 'vid'),)


class Watchdog(models.Model):
    wid = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    type = models.CharField(max_length=16)
    message = models.TextField()
    variables = models.TextField()
    severity = models.PositiveIntegerField()
    link = models.CharField(max_length=255)
    location = models.TextField()
    referer = models.TextField(blank=True, null=True)
    hostname = models.CharField(max_length=128)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'watchdog'
