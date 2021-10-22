from rest_framework import serializers
import clinical_effort.models as m
from django.contrib.auth.models import User

# Complexity value
class ComplexityTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.ComplexityTypes
        fields = '__all__'

# Complexity value
class ComplexityValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.ComplexityValues
        fields = '__all__'

# Complexity
class ComplexitySerializer(serializers.ModelSerializer):

    values = ComplexityValuesSerializer(source='complexityvalues_set', many=True, required=False)

    class Meta:
        model = m.Complexity
        fields = '__all__'


# Year values
class YearValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.YearValues
        fields = '__all__'


# Years value
class YearsSerializer(serializers.ModelSerializer):

    values = YearValuesSerializer(source='yearvalues_set', many=True, required=False)

    class Meta:
        model = m.Years
        fields = '__all__'

# Notes
class NotesSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = m.Notes
        fields = '__all__'

    def get_created_by(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


# Visit values
class VisitValuesSerializer(serializers.ModelSerializer):

    copy_visit = serializers.SerializerMethodField()

    class Meta:
        model = m.VisitValues
        fields = '__all__'

    def get_copy_visit(self, obj):
        copy = obj.visit.cycle.copy_hours
        first_cycle_visit = obj.visit.cycle.visits_set.get(cycle_number=1, visit_number=1).id
        if first_cycle_visit == obj.visit.id or copy == False:
            return ''
        else:
            return first_cycle_visit

# Personnel fields
class PersonnelFieldsSerializer(serializers.ModelSerializer):

    values = VisitValuesSerializer(source='visitvalues_set', many=True, required=False)

    class Meta:
        model = m.PersonnelFields
        fields = '__all__'


# Clinical trial instance visits
class VisitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Visits
        fields = '__all__'



# Clinical trial instance cycles
class CyclesSerializer(serializers.ModelSerializer):

    visits = VisitsSerializer(source='visits_set', many=True, required=False)

    class Meta:
        model = m.Cycles
        fields = '__all__'


# Clinical trial instance arms
class TrialArmsSerializer(serializers.ModelSerializer):

    cycles = CyclesSerializer(source='cycles_set', many=True, required=False)

    class Meta:
        model = m.TrialArms
        fields = '__all__'



# Personnel
class PersonnelSerializer(serializers.ModelSerializer):

    arm_fields = serializers.SerializerMethodField()

    class Meta:
        model = m.Personnel
        fields = '__all__'

    def get_arm_fields(self, obj):
        fields = {}
        arms = obj.instance.trialarms_set
        arms_s = TrialArmsSerializer(arms, many=True, required=False)
        for arm in arms_s.data:
            flds = obj.personnelfields_set.filter(arm=arm['id'])
            flds_s = PersonnelFieldsSerializer(flds, many=True, required=False)
            fields[arm['id']] = flds_s.data
        if arms_s:
            return fields
        else:
            return []


# Project Access types
class ProjectAccessTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.ProjectAccessTypes
        fields = '__all__'

# Project Access
class ProjectAccessSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = m.ProjectAccess
        fields = '__all__'

    def get_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


# Clinical trial effort instance
class CTEffortSerializer(serializers.ModelSerializer):

    complexity = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    arms = TrialArmsSerializer(source='trialarms_set', many=True, required=False)
    people = PersonnelSerializer(source='personnel_set', many=True, required=False)
    years = YearsSerializer(source='years_set', many=True, required=False)
    notes = NotesSerializer(source='notes_set', many=True, required=False)

    class Meta:
        model = m.CTEffort
        fields = '__all__'


    def get_complexity(self, obj):
        if m.Complexity.objects.filter(instance=obj.id).exists():
            complex_s = ComplexitySerializer(m.Complexity.objects.get(instance=obj.id), many=False, required=False)
            return complex_s.data
        else:
            return []

    def get_access(self, obj):
        relationships = obj.projectaccess_set.all().order_by('type')
        return ProjectAccessSerializer(relationships, many=True, required=False).data


# Base Clinical trial effort instance (no serializer fields)
class BaseCTEffortSerializer(serializers.ModelSerializer):

    number_arms = serializers.SerializerMethodField(read_only=True)
    number_people = serializers.SerializerMethodField(read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = m.CTEffort
        fields = '__all__'

    def get_number_arms(self, obj):
        return obj.trialarms_set.count()

    def get_number_people(self, obj):
        return obj.personnel_set.count()

    def get_created_by(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

# Cycle types
class CycleTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.CycleTypes
        fields = '__all__'


# Personnel types
class PersonnelTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.PersonnelTypes
        fields = '__all__'
