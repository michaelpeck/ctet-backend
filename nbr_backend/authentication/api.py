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

from .serializers import UserSerializer


# @api_view(['GET'])
# @permission_classes([permissions.AllowAny])
# def get_user(request):
#     user = request.user
#     return Response('')


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            return self.request.user

        return super(UserViewSet, self).get_object()
