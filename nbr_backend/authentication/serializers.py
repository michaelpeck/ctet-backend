from rest_framework import serializers
from django.contrib.auth.models import User

import authentication.models as m

# Users
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


# Users
class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']


# User profiles
class UserProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.UserProfiles
        fields = '__all__'
