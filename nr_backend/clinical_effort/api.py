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

from clinical_effort.models import CTEffort, CycleTypes, PersonnelTypes, TrialArms, Cycles, Visits, Personnel, CRCVisit, NCVisit, DCVisit, GeneralVisit
from .serializers import CTEffortSerializer, CycleTypesSerializer, PersonnelTypesSerializer, TrialArmsSerializer, CyclesSerializer, VisitsSerializer, PersonnelSerializer, CRCVisitSerializer, NCVisitSerializer, DCVisitSerializer, GeneralVisitSerializer

# Clinical trial effort Viewset
class CTEffortViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CTEffort.objects.all()
    serializer_class = CTEffortSerializer
    lookup_field = 'request_id'

    @action(detail=False, methods=['POST'])
    def submit(self, request, request_id=None):

        # Save request
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)


# Cycle types Viewset
class CycleTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CycleTypes.objects.all()
    serializer_class = CycleTypesSerializer
    lookup_field = 'request_id'


# Personnel types Viewset
class PersonnelTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = PersonnelTypes.objects.all()
    serializer_class = PersonnelTypesSerializer
    lookup_field = 'request_id'


# Clinical trial instance arms Viewset
class TrialArmsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = TrialArms.objects.all()
    serializer_class = TrialArmsSerializer
    lookup_field = 'request_id'


# Clinical trial instance cycles Viewset
class CyclesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Cycles.objects.all()
    serializer_class = CyclesSerializer
    lookup_field = 'request_id'


# Clinical trial instance visits Viewset
class VisitsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Visits.objects.all()
    serializer_class = VisitsSerializer
    lookup_field = 'request_id'


# Personnel Viewset
class PersonnelViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    lookup_field = 'request_id'


# Clinical research coordinator visits Viewset
class CRCVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CRCVisit.objects.all()
    serializer_class = CRCVisitSerializer
    lookup_field = 'request_id'


# Nurse coordinator visits Viewset
class NCVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = NCVisit.objects.all()
    serializer_class = NCVisitSerializer
    lookup_field = 'request_id'


# Data coordinator visits Viewset
class DCVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = DCVisit.objects.all()
    serializer_class = DCVisitSerializer
    lookup_field = 'request_id'


# General visit Viewset
class GeneralVisitViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = GeneralVisit.objects.all()
    serializer_class = GeneralVisitSerializer
    lookup_field = 'request_id'
