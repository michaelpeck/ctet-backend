from django.conf import settings
import csv
from datetime import datetime
import pandas as pd


from clinical_effort.models import CTEffort, ComplexityTypes, ComplexityValues
from ..serializers import CTEffortSerializer


# Get general hours summary df
def get_summary_df(proj_id):

    # Get project
    project = CTEffort.objects.get(id=proj_id)

    # Get arms and people
    arms = project.trialarms_set.all()
    people = project.personnel_set.all()

    # Dataframe
    # Assemble cols
    cols = ['person']
    index = []
    for person in people:
        index.append(person.id)
    index.append('summary')

    for arm in arms:
        cycles = arm.cycles_set.all()
        for cycle in cycles:
            visits = cycle.visits_set.all()
            for visit in visits:
                cols.append(str(visit.id))

    # Add values
    df = pd.DataFrame(index=index, columns=cols)

    # Add values
    for person in people:
        df.at[person.id, 'person'] = person.name
        for arm in arms:
            cycles = arm.cycles_set.all()
            for cycle in cycles:
                visits = cycle.visits_set.all()
                for visit in visits:
                    df.at[person.id, str(visit.id)] = 0

    return df

# Add sum values to summary df
def edit_summary_df(df, values, person):
    for key, val in values.items():
        if val != 'Sum':
            df.at[person.id, str(key)] = val
    return df

# Get hours per person per arm
def get_person_arm_hours_df(proj_id):

    # Get project
    project = CTEffort.objects.get(id=proj_id)

    # Get arms and people
    arms = project.trialarms_set.all()
    people = project.personnel_set.all()

    # Dataframe
    # Assemble cols
    index = []
    for person in people:
        index.append(person.id)

    cols = ['person']
    for arm in arms:
        cols.append(arm.id)

    # Add values
    df = pd.DataFrame(index=index, columns=cols)
    for person in people:
        df.at[person.id, 'person'] = person.name
        for arm in arms:
            df.at[person.id, arm.id] = 0

    return df

# Add sum values to summary df
def edit_person_arm_hours_df(df, values, person, arm):
    for key, val in values.items():
        if val != 'Sum':
            df.at[person.id, arm.id] = df.loc[person.id, arm.id] + val
    return df

# Subject summary df
def get_subject_summary_df(summary, people, arms):

    # Dataframe
    # Assemble cols
    cols = ['person', 'year_hours', 'hours_per_subject', 'per_subject_effort']
    index = []
    for person in people:
        index.append(person.id)
    index.append('summary')

    # Add values
    df = pd.DataFrame(index=index, columns=cols)
    for person in people:
        df.at[person.id, 'person'] = person.name
        df.at[person.id, 'year_hours'] = person.year_hours
        # Sum hours per subject
        val = 0
        for arm in arms:
            cycles = arm.cycles_set.all()
            for cycle in cycles:
                visits = cycle.visits_set.all()
                for visit in visits:
                    val += summary.loc[person.id, str(visit.id)]
        df.at[person.id, 'hours_per_subject'] = val
        df.at[person.id, 'per_subject_effort'] = val/person.year_hours

    return df


# Total summary df
def get_total_summary_df(proj_id, subject_summary, people, arms):

    # Get project
    project = CTEffort.objects.get(id=proj_id)

    # Dataframe
    # Assemble cols
    cols = ['person', 'total_hours', 'addl_lump_hours', 'addl_lump_effort', 'total_effort', 'total_miris_effort']
    index = []
    for person in people:
        index.append(person.id)
    index.append('summary')

    # Add values
    df = pd.DataFrame(index=index, columns=cols)
    for person in people:
        df.at[person.id, 'person'] = person.name
        df.at[person.id, 'total_hours'] = subject_summary.loc[person.id, 'hours_per_subject'] * project.estimated_subjects
        # Addl lump hours
        df.at[person.id, 'addl_lump_hours'] = person.addl_lump_hours
        # Addl lump effort
        df.at[person.id, 'addl_lump_effort'] = person.addl_lump_hours/person.year_hours
        # Total effort
        df.at[person.id, 'total_effort'] = (subject_summary.loc[person.id, 'hours_per_subject'] * project.estimated_subjects) + person.addl_lump_hours
        # Total miris effort
        df.at[person.id, 'total_miris_effort'] = ((subject_summary.loc[person.id, 'hours_per_subject'] * project.estimated_subjects) + person.addl_lump_hours)/person.year_hours

    return df
