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
from datetime import date

import clinical_effort.models as m
import clinical_effort.serializers as s

from authentication.models import UserProfiles

from clinical_effort.actions.project import setup_project
from clinical_effort.actions.people import add_person, update_person, add_field, add_new_person_fields, change_type
from clinical_effort.actions.arms import add_arm
from clinical_effort.actions.cycles import add_cycle, update_cycle
from clinical_effort.actions.complexity import create_complexity
from clinical_effort.actions.years import add_year_value, add_default_years

from clinical_effort.exports.export_project import create_export


# Base clinical trial effort Viewset (no serializer fields)
class BaseCTEffortViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    # queryset = CTEffort.objects.all()
    serializer_class = s.BaseCTEffortSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Set user (check if dev)
        user = self.request.user
        if settings.ENV_TYPE == 'dev':
            user = 1

        # User accesses and related projects
        accesses = m.ProjectAccess.objects.filter(user=user, type=1).values('instance')
        owned_projects = m.CTEffort.objects.filter(id__in=accesses)

        return owned_projects

# Base Shared Project Viewset (no serializer fields)
class BaseSharedCTEffortViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    # queryset = CTEffort.objects.all()
    serializer_class = s.BaseCTEffortSerializer
    lookup_field = 'id'

    def get_queryset(self):
        # Set user (check if dev)
        user = self.request.user
        if settings.ENV_TYPE == 'dev':
            user = 1

        # User accesses and related projects
        accesses = m.ProjectAccess.objects.filter(user=user, type=2).values('instance')
        related_projects = m.CTEffort.objects.filter(id__in=accesses)

        return related_projects

# Clinical trial effort Viewset
class CTEffortViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.CTEffort.objects.all()
    serializer_class = s.CTEffortSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['PUT'])
    def new(self, request, id=None):

        # Save project
        new_project = request.data
        # new_owner = { "type": 1 }

        # Eid number
        next_id = self.get_queryset().latest('created').id + 1
        id_string = f"{next_id:05}"

        # Check if dev environment and set vars accordingly
        if settings.ENV_TYPE == 'dev':
            new_project['user'] = 1
            # new_owner['user'] = 1
            new_project['eid'] = '00000-' + id_string
        else:
            new_project['user'] = self.request.user.id
            # new_owner['user'] = self.request.user.id
            email_split = self.request.user.email.split("@", 1)
            network_id = email_split[0]
            lawson_id = UserProfiles.objects.get(network_id=network_id).employee_id
            new_project['eid'] = lawson_id + '-' + id_string

        # Serialize project and save
        serializer = self.serializer_class(data=new_project)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        # Serialize project and save
        # new_owner['instance'] = serializer.data['id']
        # owner_serializer = ProjectAccessSerializer(data=new_owner)
        # if owner_serializer.is_valid(raise_exception=True):
        #     owner_serializer.save()

        # Call setup project action
        add_proj = setup_project(request.data, serializer.data['id'])

        # Call setup complexity action
        add_proj = create_complexity(serializer.data['id'])

        # Retrieve new project
        project = m.CTEffort.objects.get(id=serializer.data['id'])
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)


    @action(detail=True, methods=['PUT'])
    def add_arm(self, request, id=None):

        # get type
        type = request.data['type']

        # Create arm
        arm_cycles = []
        arm_name = ''
        if type == 1:
            arm_cycles = ['pre-screening', 'screening']
            arm_name = 'New Screening'
        elif type == 2:
            arm_cycles = ['standard', 'custom']
            arm_name = 'New Arm'
        else:
            arm_cycles = ['end-of-treatment', 'follow-up']
            arm_name = 'New Follow-up'
        arm = add_arm(name=arm_name, cycle_names=arm_cycles, type_id=type, proj_id=id)

        # Add years for arm
        years = m.CTEffort.objects.get(id=id).years_set.all()
        for year in years:
            add_year_value(year=year, arm=arm)

        # Retrieve updated project
        project = m.CTEffort.objects.get(id=id)
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)

    @action(detail=True, methods=['GET'])
    def add_person(self, request, id=None):

        # Add person
        person = add_person(proj_id=id, type_id=5, amount=1)

        # Add fields for arms
        add_new_person_fields(proj_id=id, person=person)

        # Retrieve updated project
        project = m.CTEffort.objects.get(id=id)
        p_serializer = self.serializer_class(project, many=False)

        return Response(p_serializer.data, status=200)

    @action(detail=True, methods=['GET'])
    def export(self, request, id=None):

        # Create export file
        export_path = create_export(id=id)
        return_obj = {}
        return_obj['path'] = export_path

        # if os.path.exists(export_path):
        #     with open(export_path, 'rb') as fh:
        #         response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        #         response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(export_path)
        #         return response
        # raise Http404

        return Response(return_obj, status=200)


# Complexity Viewset
class ComplexityTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.ComplexityTypes.objects.all()
    serializer_class = s.ComplexityTypesSerializer
    lookup_field = 'id'

# Complexity Viewset
class ComplexityViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.Complexity.objects.all()
    serializer_class = s.ComplexitySerializer
    lookup_field = 'id'


# Complexity Types Viewset
class ComplexityValuesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.ComplexityValues.objects.all()
    serializer_class = s.ComplexityValuesSerializer
    lookup_field = 'id'



# Cycle types Viewset
class CycleTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.CycleTypes.objects.all()
    serializer_class = s.CycleTypesSerializer
    lookup_field = 'id'


# Personnel types Viewset
class PersonnelTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.PersonnelTypes.objects.all()
    serializer_class = s.PersonnelTypesSerializer
    lookup_field = 'id'


# Clinical trial instance arms Viewset
class TrialArmsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.TrialArms.objects.all()
    serializer_class = s.TrialArmsSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['GET'])
    def add_cycle(self, request, id=None):

        # Get project
        arm = m.TrialArms.objects.filter(id=id)
        proj_id = arm[0].instance

        # Create arm
        cycle = add_cycle(type='custom', proj_id=proj_id.id, arm_id=id)

        # Retrieve updated project
        project = m.CTEffort.objects.get(id=proj_id.id)
        p_serializer = s.CTEffortSerializer(project, many=False)

        return Response(p_serializer.data, status=200)



# Clinical trial instance cycles Viewset
class CyclesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.Cycles.objects.all()
    serializer_class = s.CyclesSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['PUT'])
    def cycle_update(self, request, id=None):

        # Get project
        cycle = m.Cycles.objects.filter(id=id)
        proj_id = cycle[0].instance
        print(proj_id.id)

        # Create arm
        cycle = update_cycle(object=request.data, proj_id=proj_id.id, cycle_id=id)
        c_serializer = self.serializer_class(cycle)

        return Response(c_serializer.data, status=200)


# Years Viewset
class YearsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.Years.objects.all()
    serializer_class = s.YearsSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['GET'])
    def add_year(self, request, id=None):

        # Get project
        proj = m.CTEffort.objects.get(id=id)

        # Create arm
        new_year = add_default_years(proj_id=id)

        # Retrieve updated project
        project = m.CTEffort.objects.get(id=id)
        p_serializer = s.CTEffortSerializer(project, many=False)

        return Response(p_serializer.data, status=200)

# Year values Viewset
class YearValuesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.YearValues.objects.all()
    serializer_class = s.YearValuesSerializer
    lookup_field = 'id'


# Clinical trial instance visits Viewset
class VisitsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.Visits.objects.all()
    serializer_class = s.VisitsSerializer
    lookup_field = 'id'


# Clinical trial instance visits Viewset
class VisitValuesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.VisitValues.objects.all()
    serializer_class = s.VisitValuesSerializer
    lookup_field = 'id'

# Personnel fields Viewset
class PersonnelFieldsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.PersonnelFields.objects.all()
    serializer_class = s.PersonnelFieldsSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['GET'])
    def remove(self, request, id=None):

        # Get field
        field = self.get_object()

        # Delete field
        field.delete()

        # Get instance cycles
        instance = field.person.instance
        instance_s = s.CTEffortSerializer(instance, many=False)
        cycles = instance_s.data['cycles']

        return Response(cycles, status=200)


# Personnel Viewset
class PersonnelViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.Personnel.objects.all()
    serializer_class = s.PersonnelSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['PUT'])
    def person_update(self, request, id=None):

        # Get project
        person = m.Personnel.objects.filter(id=id)
        proj_id = person[0].instance

        # Run person update function
        new_person = update_person(object=request.data, proj_id=proj_id.id, person_id=id)
        p_serializer = self.serializer_class(new_person)

        return Response(p_serializer.data, status=200)

    @action(detail=True, methods=['POST'])
    def add_field(self, request, id=None):

        # Get project
        person = m.Personnel.objects.filter(id=id)
        proj = person[0].instance

        # amount
        amount = request.data['amount']
        arm = request.data['arm']

        # Run person update function
        for field in range(amount):
            new_field = add_field(project_id=proj.id, person_id=id, arm_id=arm)

        # Get person
        person = m.Personnel.objects.get(id=id)
        p_serializer = self.serializer_class(person)

        return Response(p_serializer.data, status=200)

    @action(detail=True, methods=['PUT'])
    def change_type(self, request, id=None):

        # Get project
        person = m.Personnel.objects.filter(id=id)
        proj_id = person[0].instance

        # Run person update function
        person = change_type(object=request.data, proj_id=proj_id.id, person_id=id)
        p_serializer = self.serializer_class(person)

        return Response(p_serializer.data, status=200)

# Notes Viewset
class NotesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.Notes.objects.all()
    serializer_class = s.NotesSerializer
    lookup_field = 'id'

# Project Access Viewset
class ProjectAccessViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.ProjectAccess.objects.all()
    serializer_class = s.ProjectAccessSerializer
    lookup_field = 'id'

# Project Access Types Viewset
class ProjectAccessTypesViewSet(viewsets.ModelViewSet):

    permission_classes = [
        settings.VIEWSET_PERMISSIONS,
    ]
    queryset = m.ProjectAccessTypes.objects.all()
    serializer_class = s.ProjectAccessTypesSerializer
    lookup_field = 'id'
