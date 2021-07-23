from django.conf import settings
import csv
from datetime import datetime
import pandas as pd

from clinical_effort.models import CTEffort, ComplexityTypes, ComplexityValues
from clinical_effort.serializers import CTEffortSerializer


# Create new project
def get_general_df(proj_id):

    # Get project
    project_vals = CTEffort.objects.filter(id=proj_id).values('name', 'protocol_number', 'accounting_number', 'pi', 'estimated_subjects', 'monitor_days', 'created', 'updated')[0]

    print(project_vals)
    # Get complexity types
    complexity_types = ComplexityTypes.objects.all()

    # Make dataframe
    titles = [
    'Project Name',
    'Protocol #',
    'Accounting #',
    'Primary Investigator',
    'Estimated Subjects',
    'Monitor Days',
    'Created At',
    'Updated At'
    ]
    cols = ['Label', 'Value']
    # cols = ['element', 'no_effort', 'minimal_effort', 'moderate_effort', 'max_effort', 'raw_score', 'weight', 'weighted_score']
    index = []
    for key, val in project_vals.items():
        index.append(key)
        print(key)
        print(val)


    df = pd.DataFrame(index=index, columns=cols)
    idx = 0
    for key, val in project_vals.items():
        df.at[key, 'Label'] = titles[idx]
        if isinstance(val, datetime):
            df.at[key, 'Value'] = val.strftime("%m/%d/%Y")
        else:
            df.at[key, 'Value'] = val
        idx += 1


    return df
