from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

import json
import io
import hashlib

from departments.models import SupportRequests, SupportContacts
from .serializers import SupportRequestSerializer, SupportContactSerializer
from .emails import supportRequestEmail

# Project Viewset
class SupportRequestViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = SupportRequests.objects.all()
    serializer_class = SupportRequestSerializer
    lookup_field = 'request_id'

    @action(detail=False, methods=['POST'])
    def submit(self, request, request_id=None):

        print(request.data)

        # Save request
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Get contact
        contact = SupportContacts.objects.filter(contact_id=request.data['contact'])
        contact_serializer = SupportContactSerializer(contact[0], many=False)

        print(contact_serializer.data)
        # Send email
        to_email = [contact_serializer.data['email']]
        subject = contact_serializer.data['type_name'] + " - Support Request"
        from_email = settings.EMAIL_HOST_USER
        supportRequestEmail(subject, from_email, to_email, serializer.data, contact_serializer.data['type_name'])

        return Response('All good', status=200)
