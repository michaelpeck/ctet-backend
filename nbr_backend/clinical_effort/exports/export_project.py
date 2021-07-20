import pandas as pd
from datetime import datetime
from django.conf import settings
# import StringIO

from clinical_effort.models import CTEffort, TrialArms
from ..serializers import CTEffortSerializer

from .complexity_df import get_complexity_df
from .person_arm_df import get_person_arm_df
from .structure_df import get_structure_df
from .time_allocations import get_summary_df, edit_summary_df, get_subject_summary_df, get_total_summary_df
from .summary import get_summary_fte_df

# Create new project
def create_export(id):

    # Create dataframes and format dates
    # Project
    df_project = pd.DataFrame.from_records(CTEffort.objects.filter(id=id).values('name', 'protocol_number', 'accounting_number', 'pi', 'estimated_subjects', 'monitor_days', 'created', 'updated'))
    df_project['created'] = df_project['created'].dt.tz_localize(None)
    df_project['updated'] = df_project['updated'].dt.tz_localize(None)

    # Personnel
    df_personnel = pd.DataFrame.from_records(CTEffort.objects.filter(id=id)[0].personnel_set.values('name', 'amount', 'year_hours', 'addl_lump_hours', 'updated'))
    df_personnel['updated'] = df_personnel['updated'].dt.tz_localize(None)

    # Structure
    df_arms = pd.DataFrame.from_records(CTEffort.objects.filter(id=id)[0].trialarms_set.values('name', 'estimated_duration', 'updated'))
    df_arms['updated'] = df_arms['updated'].dt.tz_localize(None)

    # Time

    # Complexity

    # Summary

    # Create file
    now = datetime.now()
    filepath = settings.MEDIA_ROOT + 'exports/ctet_' + id + '_export_' + now.strftime("%m%d%Y") + '_' + now.strftime("%H%M%S") + '.xlsx'

    # Create sheet
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        # Project
        df_project.to_excel(writer, sheet_name='general', index=False)

        # Personnel
        df_personnel.to_excel(writer, sheet_name='personnel', index=False)

        # Structure
        arms = CTEffort.objects.filter(id=id)[0].trialarms_set.all()
        row_index = 0
        for arm in arms:
            # Add arm name row
            arm_name = pd.DataFrame(columns=[arm.name])
            arm_name.to_excel(writer, sheet_name='structure', index=False, startrow=row_index)
            row_index += 1
            # Get and add arm cycle df
            structure_df = get_structure_df(id, arm)
            structure_df.to_excel(writer, sheet_name='structure', index=False, startrow=row_index)
            row_index += structure_df.shape[0] + 2

        # Time Allocations
        people = CTEffort.objects.filter(id=id)[0].personnel_set.all()
        arms = CTEffort.objects.filter(id=id)[0].trialarms_set.all()
        row_index = 0
        summary_df = get_summary_df(id)
        for person in people:
            person_name = pd.DataFrame(columns=[person.name])
            person_name.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
            row_index += 1
            for arm in arms:
                arm_name = pd.DataFrame(columns=[arm.name])
                arm_name.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
                row_index += 1
                p_a_df = get_person_arm_df(id, person.id, arm.id)
                p_a_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
                row_index += p_a_df.shape[0] + 2
                summary_df = edit_summary_df(summary_df, p_a_df.loc['sum'], person)
                # summary_df.at[person.id, str]
        # Summary table
        summary_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        row_index += summary_df.shape[0] + 2
        # Subject summary
        subject_summary_df = get_subject_summary_df(summary_df, people, arms)
        subject_summary_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        row_index += subject_summary_df.shape[0] + 2
        # Total summary
        total_summary_df = get_total_summary_df(id, subject_summary_df, people, arms)
        total_summary_df.to_excel(writer, sheet_name='time_allocations', index=False, startrow=row_index)
        row_index += total_summary_df.shape[0] + 2
        # Complexity
        df_complexity = get_complexity_df(id)
        df_complexity.to_excel(writer, sheet_name='complexity', index=False)
        # Summary
        df_fte = get_summary_fte_df(total_summary_df, df_complexity, people)
        df_fte.to_excel(writer, sheet_name='summary', index=False)


    # Get media root for download
    mediapath = settings.MEDIA_URL + 'exports/' + filepath.split('/')[-1]

    return mediapath
