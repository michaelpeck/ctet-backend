from rest_framework import serializers
from departments.models import SupportContacts, SupportRequests


# Support Contacts
class SupportContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportContacts
        fields = '__all__'

# Support Requests
class SupportRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportRequests
        fields = '__all__'
