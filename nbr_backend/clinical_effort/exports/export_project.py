import pandas as pd
from datetime import datetime
from django.conf import settings
# import StringIO

from clinical_effort.models import CTEffort, TrialArms
from ..serializers import CTEffortSerializer


# Create new project
def create_export(id):

    # Create dataframes and format dates
    # Project
    df_project = pd.DataFrame.from_records(CTEffort.objects.filter(id=id).values('name', 'protocol_number', 'accounting_number', 'pi', 'estimated_subjects', 'monitor_days', 'created', 'updated'))
    df_project['created'] = df_project['created'].dt.tz_localize(None)
    df_project['updated'] = df_project['updated'].dt.tz_localize(None)

    # Personnel
    df_personnel = pd.DataFrame.from_records(CTEffort.objects.filter(id=id)[0].personnel_set.values('type', 'name', 'amount', 'year_hours', 'addl_lump_hours', 'updated'))
    df_personnel['updated'] = df_arms['updated'].dt.tz_localize(None)

    # Structure
    df_arms = pd.DataFrame.from_records(CTEffort.objects.filter(id=id)[0].trialarms_set.values('type', 'name', 'estimated_duration', 'updated'))
    df_arms['updated'] = df_arms['updated'].dt.tz_localize(None)

    # Time

    # Complexity

    # Summary

    # Create file
    now = datetime.now()
    filepath = settings.MEDIA_ROOT + 'exports/ctet_' + id + '_export_' + now.strftime("%m%d%Y") + '_' + now.strftime("%H%M%S") + '.xlsx'

    # Create sheet
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        df_project.to_excel(writer, sheet_name='general', index=False)
        df_personnel.to_excel(writer, sheet_name='personnel', index=False)
        df_arms.to_excel(writer, sheet_name='structure', index=False)

    # Get media root for download
    mediapath = settings.MEDIA_URL + 'exports/' + filepath.split('/')[-1]

    return mediapath
