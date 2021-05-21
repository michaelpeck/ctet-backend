from rest_framework import serializers
from clinical_effort.models import CTEffort, CycleTypes, PersonnelTypes, TrialArms, Cycles, Visits, Personnel
from clinical_effort.models import Complexity, ComplexityValue, ComplexityTypes

# Complexity value
class ComplexityTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplexityTypes
        fields = '__all__'

# Complexity value
class ComplexityValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplexityValue
        fields = '__all__'

# Complexity
class ComplexitySerializer(serializers.ModelSerializer):

    values = serializers.SerializerMethodField()

    class Meta:
        model = Complexity
        fields = '__all__'

    def get_values(self, obj):
        vals = obj.complexityvalue_set
        val_s = ComplexityValueSerializer(vals, many=True, required=False)
        if val_s:
            return val_s.data
        else:
            return []

# Personnel
class PersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personnel
        fields = '__all__'

# Clinical trial instance visits
class VisitsSerializer(serializers.ModelSerializer):

    visits = serializers.SerializerMethodField()

    class Meta:
        model = Visits
        fields = '__all__'

    def get_visits(self, obj):
        visits = {}
        people = obj.instance.personnel_set.all()
        # for person in people:
        #     fields
        #     if VisitValue.objects.filter(visit=obj.id, ).exists():
        #         crc_s = CRCVisitSerializer(CRCVisit.objects.get(visit=obj.id), many=False, required=False)
        #         visits['crc'] = crc_s.data
        #     else:
        #         visits['crc'] = {}
        #
        # if NCVisit.objects.filter(visit=obj.id).exists():
        #     nc_s = NCVisitSerializer(NCVisit.objects.get(visit=obj.id), many=False, required=False)
        #     visits['nc'] = nc_s.data
        # else:
        #     visits['nc'] = {}
        #
        # if DCVisit.objects.filter(visit=obj.id).exists():
        #     dc_s = DCVisitSerializer(DCVisit.objects.get(visit=obj.id), many=False, required=False)
        #     visits['dc'] = dc_s.data
        # else:
        #     visits['dc'] = {}
        #
        # if GeneralVisit.objects.filter(visit=obj.id).exists():
        #     ls_s = GeneralVisitSerializer(GeneralVisit.objects.get(visit=obj.id), many=False, required=False)
        #     visits['ls'] = ls_s.data
        # else:
        #     visits['ls'] = {}


        return visits


# Clinical trial instance cycles
class CyclesSerializer(serializers.ModelSerializer):

    visits = serializers.SerializerMethodField()

    class Meta:
        model = Cycles
        fields = '__all__'

    def get_visits(self, obj):
        vis = obj.visits_set
        vis_s = VisitsSerializer(vis, many=True, required=False)
        if vis_s:
            return vis_s.data
        else:
            return []

# Clinical trial instance arms
class TrialArmsSerializer(serializers.ModelSerializer):

    cycles = CyclesSerializer(source='cycles_set', many=True, required=False)

    class Meta:
        model = TrialArms
        fields = '__all__'




# Clinical trial effort instance
class CTEffortSerializer(serializers.ModelSerializer):
    #
    cycles = serializers.SerializerMethodField()
    pre_cycles = serializers.SerializerMethodField()
    post_cycles = serializers.SerializerMethodField()
    complexity = serializers.SerializerMethodField()


    # pre_cycles = CyclesSerializer(source='cycles_set', queryset=Cycles.objects.filter(type_id__in = [1, 2]), many=True, required=False)
    # post_cycles = CyclesSerializer(source='cycles_set', queryset=Cycles.objects.filter(type_id__in = [4, 5]), many=True, required=False)
    # cycles = CyclesSerializer(source='cycles_set', many=True, required=False)
    arms = TrialArmsSerializer(source='trialarms_set', many=True, required=False)
    people = PersonnelSerializer(source='personnel_set', many=True, required=False)

    class Meta:
        model = CTEffort
        fields = '__all__'

    def get_cycles(self, obj):
        pre = obj.cycles_set.filter(type_id__in = [1, 2])
        pre_s = CyclesSerializer(pre, many=True, required=False)
        post = obj.cycles_set.filter(type_id__in = [4, 5])
        post_s = CyclesSerializer(post, many=True, required=False)
        arms = obj.trialarms_set
        arms_s = TrialArmsSerializer(arms, many=True, required=False)
        arm_cycles=[]
        for arm in arms_s.data:
            # print(arm["cycles"])
            for cycle in arm["cycles"]:
                arm_cycles.append(cycle)
        cycles = pre_s.data + arm_cycles + post_s.data
        if cycles:
            return cycles
        else:
            return []


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

    def get_complexity(self, obj):
        if Complexity.objects.filter(instance=obj.id).exists():
            complex_s = ComplexitySerializer(Complexity.objects.get(instance=obj.id), many=False, required=False)
            return complex_s.data
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
