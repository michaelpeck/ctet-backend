from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User

import json
import io

import authentication.models as m
import authentication.serializers as s



class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = User.objects.all()
    serializer_class = s.UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserViewSet, self).get_object()

class UsersViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = User.objects.all()
    serializer_class = s.UsersSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UsersViewSet, self).get_object()

class UserProfilesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.UserProfiles.objects.all()
    serializer_class = s.UserProfilesSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            email_split = self.request.user.email.split("@", 1)
            network_id = email_split[0]
            profile = m.UserProfiles.objects.get(network_id=network_id)
            return profile

        return super(UserProfilesViewSet, self).get_object()
