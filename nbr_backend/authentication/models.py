from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from django.utils import timezone
import datetime

from .managers import CustomUserManager

# Clone field function to get fields from AbstractBaseUser
def clone_field(model_class, name, **kwargs):
    name, klass_path, fargs, fkwargs = model_class._meta.get_field(name).deconstruct()
    fkwargs.update(kwargs)
    field_class = import_string(klass_path)
    return field_class(*fargs, **fkwargs)


# User models
class User(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    username = clone_field(AbstractUser, 'username', db_column='name')
    password = clone_field(AbstractBaseUser, 'password', db_column='pass')
    mail = models.CharField(max_length=64, blank=True, null=True)
    signature = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    is_active = clone_field(AbstractUser, 'is_active', db_column='status')
    is_admin = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)


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




# Users model (SNAP users)
class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    mail = models.CharField(max_length=64, blank=True, null=True)
    is_admin = models.BooleanField(default = False)

    class Meta:
        managed = False
        db_table = 'users'
