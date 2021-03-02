from rest_framework import serializers
from departments.models import SupportContacts, SupportRequests


# Support Contacts
class SupportContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportContacts
        fields = '__all__'

# Support Requests
class SupportRequestSerializer(serializers.ModelSerializer):

    # nbr = serializers.SerializerMethodField()

    class Meta:
        model = SupportRequests
        fields = '__all__'

    # def get_nbr(self, obj):
    #     qry = RspProjStatusLog.objects.filter(status_type_id=13, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
    #     if qry:
    #         status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
    #         return [13, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
    #     else:
    #         return [13, '', '', '']
