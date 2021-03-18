from rest_framework import serializers
from clinical_effort.models import CTEffort, CycleTypes, PersonnelTypes, TrialArms, Cycles, Visits, Personnel, CRCVisit, NCVisit, DCVisit, GeneralVisit

# Clinical trial instance cycles
class CyclesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cycles
        fields = '__all__'

# Clinical trial instance arms
class TrialArmsSerializer(serializers.ModelSerializer):

    cycles = CyclesSerializer(source='cycles_set', many=True, required=False)

    class Meta:
        model = TrialArms
        fields = '__all__'


# Clinical trial effort instance
class CTEffortSerializer(serializers.ModelSerializer):
    #
    pre_cycles = serializers.SerializerMethodField()
    post_cycles = serializers.SerializerMethodField()


    # pre_cycles = CyclesSerializer(source='cycles_set', queryset=Cycles.objects.filter(type_id__in = [1, 2]), many=True, required=False)
    # post_cycles = CyclesSerializer(source='cycles_set', queryset=Cycles.objects.filter(type_id__in = [4, 5]), many=True, required=False)
    cycles = CyclesSerializer(source='cycles_set', many=True, required=False)
    arms = TrialArmsSerializer(source='trialarms_set', many=True, required=False)

    class Meta:
        model = CTEffort
        fields = '__all__'


    def get_pre_cycles(self, obj):
        cycles = obj.cycles_set.filter(type_id__in = [1, 2])
        cycles_s = CyclesSerializer(cycles, many=True, required=False)
        if cycles_s:
            return cycles_s.data
        else:
            return []

    def get_post_cycles(self, obj):
        cycles = obj.cycles_set.filter(type_id__in = [4, 5])
        cycles_s = CyclesSerializer(cycles, many=True, required=False)
        if cycles_s:
            return cycles_s.data
        else:
            return []



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


# Clinical trial instance visits
class VisitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visits
        fields = '__all__'


# Personnel
class PersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personnel
        fields = '__all__'

# Clinical research coordinator visits
class CRCVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = CRCVisit
        fields = '__all__'


# Nurse coordinator visits
class NCVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = NCVisit
        fields = '__all__'


# Data coordinator visits
class DCVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = DCVisit
        fields = '__all__'


# General visit
class GeneralVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralVisit
        fields = '__all__'
