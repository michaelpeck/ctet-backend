from django.conf import settings
import csv
from datetime import datetime
import pandas as pd


from clinical_effort.models import CTEffort, ComplexityTypes, ComplexityValues
from ..serializers import CTEffortSerializer


# Get total FTE table
def get_summary_fte_df(total_summary_df, complexity_df, people):

    # Dataframe
    # Instantiate cols and indexes
    cols = ['person', 'low', 'adjustment', 'high']
    index = []
    for person in people:
        index.append(person.id)

    df = pd.DataFrame(index=index, columns=cols)

    for person in people:
        df.at[person.id, 'person'] = person.name
        df.at[person.id, 'low'] = total_summary_df.loc[person.id, 'total_miris_effort']
        df.at[person.id, 'adjustment'] = complexity_df.loc['adjustment', 'weighted_score']
        df.at[person.id, 'high'] = total_summary_df.loc[person.id, 'total_miris_effort'] * complexity_df.loc['adjustment', 'weighted_score']


    return df
