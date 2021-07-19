from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, Http404

import json
import io
import os
import hashlib

from clinical_effort.models import Complexity, ComplexityValues, ComplexityTypes, Years, YearValues
from clinical_effort.models import CTEffort, CycleTypes, PersonnelTypes, TrialArms, Cycles, Visits, VisitValues, Personnel, PersonnelFields
from .serializers import CTEffortSerializer, BaseCTEffortSerializer, CycleTypesSerializer, PersonnelTypesSerializer, TrialArmsSerializer, CyclesSerializer, VisitsSerializer, VisitValuesSerializer, PersonnelSerializer, PersonnelFieldsSerializer, ComplexityValuesSerializer, ComplexitySerializer, ComplexityTypesSerializer, YearsSerializer, YearValuesSerializer

from clinical_effort.actions.project import setup_project
from clinical_effort.actions.people import add_person, update_person, add_field, add_new_person_fields
from clinical_effort.actions.arms import add_arm
from clinical_effort.actions.cycles import add_cycle, update_cycle
from clinical_effort.actions.complexity import create_complexity
from clinical_effort.actions.years import add_year_value, add_default_years

from clinical_effort.exports.export_project import create_export

# Base clinical trial effort Viewset (no serializer fields)
class BaseCTEffortViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CTEffort.objects.all()
    serializer_class = BaseCTEffortSerializer
    lookup_field = 'id'

# Clinical trial effort Viewset
class CTEffortViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CTEffort.objects.all()
    serializer_class = CTEffortSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['PUT'])
    def new(self, request, id=None):

        # Save project
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Call setup project action
        add_proj = setup_project(request.data, serializer.data['id'])

        # Call setup complexity action
        add_proj = create_complexity(serializer.data['id'])

        # Retrieve new project
        project = CTEffort.objects.get(id=serializer.data['id'])
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)


    @action(detail=True, methods=['GET'])
    def add_arm(self, request, id=None):

        # Create arm
        arm_cycles = ['standard', 'custom']
        arm = add_arm(name='New Arm', cycle_names=arm_cycles, type_id=2, proj_id=id)

        # Add years for arm
        years = CTEffort.objects.get(id=id).years_set.all()
        for year in years:
            add_year_value(year=year, arm=arm)

        # Retrieve updated project
        project = CTEffort.objects.get(id=id)
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)

    @action(detail=True, methods=['GET'])
    def add_person(self, request, id=None):

        # Add person
        person = add_person(proj_id=id, type_id=5, amount=1)

        # Add fields for arms
        add_new_person_fields(proj_id=id, person=person)

        # Retrieve updated project
        project = CTEffort.objects.get(id=id)
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)

    @action(detail=True, methods=['GET'])
    def export(self, request, id=None):

        # Create export file
        print(id)
        export_path = create_export(id=id)
        return_obj = {}
        return_obj['path'] = export_path

        # if os.path.exists(export_path):
        #     with open(export_path, 'rb') as fh:
        #         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        #         response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(export_path)
        #         return response
        # raise Http404

        # # Retrieve updated project
        # project = CTEffort.objects.get(id=id)
        # p_serializer = self.serializer_class(project, many=False)
        #
        return Response(return_obj, status=200)


# Complexity Viewset
class ComplexityTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = ComplexityTypes.objects.all()
    serializer_class = ComplexityTypesSerializer
    lookup_field = 'id'

# Complexity Viewset
class ComplexityViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Complexity.objects.all()
    serializer_class = ComplexitySerializer
    lookup_field = 'id'


# Complexity Types Viewset
class ComplexityValuesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = ComplexityValues.objects.all()
    serializer_class = ComplexityValuesSerializer
    lookup_field = 'id'



# Cycle types Viewset
class CycleTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = CycleTypes.objects.all()
    serializer_class = CycleTypesSerializer
    lookup_field = 'id'


# Personnel types Viewset
class PersonnelTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = PersonnelTypes.objects.all()
    serializer_class = PersonnelTypesSerializer
    lookup_field = 'id'


# Clinical trial instance arms Viewset
class TrialArmsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = TrialArms.objects.all()
    serializer_class = TrialArmsSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['GET'])
    def add_cycle(self, request, id=None):

        # Get project
        arm = TrialArms.objects.filter(id=id)
        proj_id = arm[0].instance

        # Create arm
        cycle = add_cycle(type='custom', proj_id=proj_id.id, arm_id=id)

        # Retrieve updated project
        project = CTEffort.objects.get(id=proj_id.id)
        p_serializer = CTEffortSerializer(project, many=False)

        return Response(p_serializer.data, status=200)


    @action(detail=False, methods=['GET'])
    def new_cycle(self, request, id=None):
        arm = self.queryset.filter(id=id)[0]
        add_cycle(type='custom', proj_id=arm.instance, arm_id=id)

        return Response('Worked', status=200)



# Clinical trial instance cycles Viewset
class CyclesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Cycles.objects.all()
    serializer_class = CyclesSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['PUT'])
    def cycle_update(self, request, id=None):

        # Get project
        cycle = Cycles.objects.filter(id=id)
        proj_id = cycle[0].instance
        print(proj_id.id)

        # Create arm
        cycle = update_cycle(object=request.data, proj_id=proj_id.id, cycle_id=id)

        # Retrieve updated project
        project = CTEffort.objects.get(id=proj_id.id)
        p_serializer = CTEffortSerializer(project, many=False)

        return Response(p_serializer.data, status=200)


# Years Viewset
class YearsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Years.objects.all()
    serializer_class = YearsSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['GET'])
    def add_year(self, request, id=None):

        # Get project
        # year = Years.objects.get(id=id)
        proj = CTEffort.objects.get(id=id)

        # Create arm
        new_year = add_default_years(proj_id=id)

        # Retrieve updated project
        project = CTEffort.objects.get(id=id)
        p_serializer = CTEffortSerializer(project, many=False)

        return Response(p_serializer.data, status=200)

# Year values Viewset
class YearValuesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = YearValues.objects.all()
    serializer_class = YearValuesSerializer
    lookup_field = 'id'


# Clinical trial instance visits Viewset
class VisitsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Visits.objects.all()
    serializer_class = VisitsSerializer
    lookup_field = 'id'


# Clinical trial instance visits Viewset
class VisitValuesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = VisitValues.objects.all()
    serializer_class = VisitValuesSerializer
    lookup_field = 'id'

# Personnel fields Viewset
class PersonnelFieldsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = PersonnelFields.objects.all()
    serializer_class = PersonnelFieldsSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['GET'])
    def remove(self, request, id=None):

        # Get field
        field = self.get_object()

        # Get instance cycles
        instance = field.person.instance
        instance_s = CTEffortSerializer(instance, many=False)
        cycles = instance_s.data['cycles']

        # Delete field
        field.delete()


        return Response(cycles, status=200)


# Personnel Viewset
class PersonnelViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['PUT'])
    def person_update(self, request, id=None):

        # Get project
        person = Personnel.objects.filter(id=id)
        proj_id = person[0].instance
        print(proj_id.id)

        # Run person update function
        new_person = update_person(object=request.data, proj_id=proj_id.id, person_id=id)

        # Retrieve updated project
        project = CTEffort.objects.get(id=proj_id.id)
        p_serializer = CTEffortSerializer(project, many=False)

        return Response(p_serializer.data, status=200)

    @action(detail=True, methods=['POST'])
    def add_field(self, request, id=None):

        # Get project
        person = Personnel.objects.filter(id=id)
        proj = person[0].instance

        # amount
        amount = request.data['amount']
        arm = request.data['arm']

        # Run person update function
        for field in range(amount):
            new_field = add_field(project_id=proj.id, person_id=id, arm_id=arm)

        # Retrieve updated project
        project = CTEffort.objects.get(id=proj.id)
        p_serializer = CTEffortSerializer(project, many=False)

        return Response(p_serializer.data, status=200)
