from django.db.models import Q
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
    lookup_field = 'cte_id'

    @action(detail=True, methods=['GET'])
    def add_arm(self, request, cte_id=None):

        project = CTEffort.objects.get(cte_id=cte_id)

        # Create arm
        arm = TrialArms(instance=project, name='New Arm')
        arm.save()

        # Add cycles for arm 1
        arm_cycles = ['standard', 'custom']
        for cycle in arm_cycles:
            cycle_type = CycleTypes.objects.get(type=cycle)
            new_cycle = Cycles(instance=project, arm=arm, type=cycle_type, number_cycles=1, name=cycle_type.name)
            new_cycle.save()

        project = CTEffort.objects.get(cte_id=cte_id)
        p_serializer = self.serializer_class(project, many=False)
        print('I made it')
        print(p_serializer.data)


        return Response(p_serializer.data, status=200)

    @action(detail=False, methods=['PUT'])
    def new(self, request, cte_id=None):

        # Save project
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        project = CTEffort.objects.get(cte_id=serializer.data['cte_id'])

        # Create general project cycles
        standard_cycles = ['pre-screening', 'screening', 'end-of-treatment', 'follow-up']
        for cycle in standard_cycles:
            cycle_type = CycleTypes.objects.get(type=cycle)
            new_cycle = Cycles(instance=project, type=cycle_type, number_cycles=1, name=cycle_type.name)
            new_cycle.save()

        # Create 1 arm
        arm_1 = TrialArms(instance=project, name='Arm 1')
        arm_1.save()

        # Add cycles for arm 1
        arm_cycles = ['standard', 'custom']
        for cycle in arm_cycles:
            cycle_type = CycleTypes.objects.get(type=cycle)
            new_cycle = Cycles(instance=project, arm=arm_1, type=cycle_type, number_cycles=1, name=cycle_type.name)
            new_cycle.save()

        project = CTEffort.objects.get(cte_id=serializer.data['cte_id'])
        cycles = project.cycles_set.all()
        p_serializer = self.serializer_class(project, many=False)
        c_serializer = CyclesSerializer(cycles, many=True)

        pre_cycles = project.cycles_set.filter(type_id__in = [1, 2])
        post_cycles = project.cycles_set.filter(type_id__in = [4, 5])
        pre_cycles_serializer = CyclesSerializer(pre_cycles, many=True)
        post_cycles_serializer = CyclesSerializer(post_cycles, many=True)

        send_back = p_serializer.data

        send_back['cycles'] = c_serializer.data
        send_back['pre_cycles'] = pre_cycles_serializer.data
        send_back['post_cycles'] = post_cycles_serializer.data
        print(p_serializer.data)

        return Response(send_back, status=200)




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
    lookup_field = 'ta_id'

    # @action(detail=False, methods=['GET'])
    # def remove(self, request, ta_id=None):
    #
    #
    #     # Save project
    #     arm = self.queryset.filter(ta_id=ta_id)[0]
    #     serializer = self.serializer_class(data=arm)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     serializer.is_valid(raise_exception=True)
    #     serializer.delete()
    #
    #     project = CTEffort.objects.get(cte_id=proj_id)
    #
    #     p_serializer = CTEffortSerializer(project, many=False)
    #
    #     return Response(p_serializer, status=200)


# Clinical trial instance cycles Viewset
class CyclesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Cycles.objects.all()
    serializer_class = CyclesSerializer
    lookup_field = 'c_id'


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
