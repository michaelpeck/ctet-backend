from rest_framework import serializers
from clinical_effort.models import CTEffort, CycleTypes, PersonnelTypes, TrialArms, Cycles, Visits, Personnel, CRCVisit, NCVisit, DCVisit, GeneralVisit


# Clinical trial effort instance
class CTEffortSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTEffort
        fields = '__all__'



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

# Clinical trial instance arms
class TrialArmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrialArms
        fields = '__all__'


# Clinical trial instance cycles
class CyclesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cycles
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
