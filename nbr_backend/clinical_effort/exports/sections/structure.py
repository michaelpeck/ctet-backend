from django.conf import settings
import csv
from datetime import datetime
import pandas as pd


from clinical_effort.models import CTEffort, ComplexityTypes, ComplexityValues
from clinical_effort.serializers import CTEffortSerializer


# Create new project
def get_structure_df(proj_id, arm):

    # Get project
    project = CTEffort.objects.get(id=proj_id)

    # Get arms
    cycles = arm.cycles_set.all()

    # Make dataframe
    cols = ['cycle_name', 'number_cycles', 'number_visits', 'copy_effort']
    df = pd.DataFrame(columns=cols)
    for cycle in cycles:
        row = {'cycle_name': cycle.name, 'number_cycles': cycle.number_cycles, 'number_visits': cycle.number_visits, 'copy_effort': cycle.copy_hours }
        df = df.append(row, ignore_index=True)

    return df
