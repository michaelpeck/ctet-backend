from django.conf import settings
import csv
from datetime import datetime


from clinical_effort.models import CTEffort, CycleTypes, Cycles
from ..serializers import CTEffortSerializer


# Create new project
def create_export(id):

    # Get project
    project = CTEffort.objects.get(id=id)

    # Create file
    now = datetime.now()
    filepath = settings.MEDIA_ROOT + '/exports/ctet_' + project.id + '_export_' + now.strftime("%m%d%Y") + '_' + now.strftime("%H%M%S") + '.csv'



    project = CTEffort.objects.get(id=id)
    serializer = CTEffortSerializer(project, many=False)


# Update all project cycles
# def update_cycles(object, id=None):
