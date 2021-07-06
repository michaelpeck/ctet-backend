from rest_framework import serializers
from clinical_effort.models import CTEffort, CycleTypes, PersonnelTypes, TrialArms, Cycles, Visits, VisitValues, Personnel, PersonnelFields
from clinical_effort.models import Complexity, ComplexityValues, ComplexityTypes, Years, YearValues

# Complexity value
class ComplexityTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplexityTypes
        fields = '__all__'

# Complexity value
class ComplexityValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplexityValues
        fields = '__all__'

# Complexity
class ComplexitySerializer(serializers.ModelSerializer):

    values = ComplexityValuesSerializer(source='complexityvalues_set', many=True, required=False)

    class Meta:
        model = Complexity
        fields = '__all__'


# Year values
class YearValuesSerializer(serializers.ModelSerializer):

    # copy_visit = serializers.SerializerMethodField()

    class Meta:
        model = YearValues
        fields = '__all__'

    # def get_copy_visit(self, obj):
    #     copy = obj.visit.cycle.copy_hours
    #     first_cycle_visit = obj.visit.cycle.visits_set.get(cycle_number=1, visit_number=1).id
    #     if first_cycle_visit == obj.visit.id:
    #         return ''
    #     else:
    #         return first_cycle_visit


# Years value
class YearsSerializer(serializers.ModelSerializer):

    values = YearValuesSerializer(source='yearvalues_set', many=True, required=False)

    class Meta:
        model = Years
        fields = '__all__'


# Visit values
class VisitValuesSerializer(serializers.ModelSerializer):

    copy_visit = serializers.SerializerMethodField()

    class Meta:
        model = VisitValues
        fields = '__all__'

    def get_copy_visit(self, obj):
        copy = obj.visit.cycle.copy_hours
        first_cycle_visit = obj.visit.cycle.visits_set.get(cycle_number=1, visit_number=1).id
        if first_cycle_visit == obj.visit.id:
            return ''
        else:
            return first_cycle_visit

# Personnel fields
class PersonnelFieldsSerializer(serializers.ModelSerializer):

    values = VisitValuesSerializer(source='visitvalues_set', many=True, required=False)

    class Meta:
        model = PersonnelFields
        fields = '__all__'




# Clinical trial instance visits
class VisitsSerializer(serializers.ModelSerializer):

    # visits = serializers.SerializerMethodField()

    class Meta:
        model = Visits
        fields = '__all__'

    # def get_visits(self, obj):
    #     visits = {}
    #     people = obj.instance.personnel_set.all()
    #     for person in people:
    #         # Initiate new visit
    #         new_vis = []
    #         # Get fields for person
    #         person_fields = person.personnelfields_set.all()
    #         # Loop through firlds and assemble visit
    #         for field in person_fields:
    #
    #             if VisitValues.objects.filter(visit=obj.id, field=field).exists():
    #                 # print('yo')
    #                 # print(VisitValuesSerializer(VisitValues.objects.filter(visit=obj.id, field=field), many=True).data)
    #                 vis_val = VisitValuesSerializer(VisitValues.objects.get(visit=obj.id, field=field), many=False, required=True)
    #                 new_vis.append(vis_val.data)
    #
    #         visits[person.id] = new_vis
    #
    #     return visits


# Clinical trial instance cycles
class CyclesSerializer(serializers.ModelSerializer):

    visits = VisitsSerializer(source='visits_set', many=True, required=False)

    class Meta:
        model = Cycles
        fields = '__all__'


# Clinical trial instance arms
class TrialArmsSerializer(serializers.ModelSerializer):

    cycles = CyclesSerializer(source='cycles_set', many=True, required=False)

    class Meta:
        model = TrialArms
        fields = '__all__'



# Personnel
class PersonnelSerializer(serializers.ModelSerializer):

    arm_fields = serializers.SerializerMethodField()

    class Meta:
        model = Personnel
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



# Clinical trial effort instance
class CTEffortSerializer(serializers.ModelSerializer):

    complexity = serializers.SerializerMethodField()
    # arms = serializers.SerializerMethodField()

    arms = TrialArmsSerializer(source='trialarms_set', many=True, required=False)
    # complexity = ComplexitySerializer(source='complexity_set', many=False, required=False)
    people = PersonnelSerializer(source='personnel_set', many=True, required=False)
    years = YearsSerializer(source='years_set', many=True, required=False)

    class Meta:
        model = CTEffort
        fields = '__all__'


    def get_complexity(self, obj):
        if Complexity.objects.filter(instance=obj.id).exists():
            complex_s = ComplexitySerializer(Complexity.objects.get(instance=obj.id), many=False, required=False)
            return complex_s.data
        else:
            return []

    def get_arms(self, obj):
        arms = obj.trialarms_set.all().order_by('type')
        return TrialArmsSerializer(arms, many=True, required=False).data


# Base Clinical trial effort instance (no serializer fields)
class BaseCTEffortSerializer(serializers.ModelSerializer):


    number_arms = serializers.SerializerMethodField(read_only=True)
    number_people = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CTEffort
        fields = '__all__'

    def get_number_arms(self, obj):
        return obj.trialarms_set.count()

    def get_number_people(self, obj):
        return obj.personnel_set.count()

# Cycle types
class CycleTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleTypes
        fields = '__all__'


# Personnel types
class PersonnelTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonnelTypes
        fields = '__all__'
