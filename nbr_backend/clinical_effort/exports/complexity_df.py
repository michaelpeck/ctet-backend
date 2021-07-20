from django.conf import settings
import csv
from datetime import datetime
import pandas as pd


from clinical_effort.models import CTEffort, ComplexityTypes, ComplexityValues
from ..serializers import CTEffortSerializer


# Create new project
def get_complexity_df(proj_id):

    # Get project
    project = CTEffort.objects.get(id=proj_id)

    # Get complexity types
    complexity_types = ComplexityTypes.objects.all()

    # Make dataframe
    titles = ['Element', 'No Effort (0pts)', 'Minimal Effort (1pts)', 'Moderate Effort (2pts)', 'Max Effort (3pts)', 'Raw Score', 'Weight', 'Weighted Score']
    cols = ['element', 'no_effort', 'minimal_effort', 'moderate_effort', 'max_effort', 'raw_score', 'weight', 'weighted_score']
    index = []
    for type in complexity_types:
        index.append(type.id)
    index.append('sum')
    index.append('adjustment')
    df = pd.DataFrame(columns=cols)
    raw_sum = 0
    weighted_sum = 0
    for type in complexity_types:
        df.at[type.id, 'element'] = type.name
        df.at[type.id, 'no_effort'] = type.zero
        df.at[type.id, 'minimal_effort'] = type.one
        df.at[type.id, 'moderate_effort'] = type.two
        df.at[type.id, 'max_effort'] = type.three
        val = ComplexityValues.objects.get(complexity=project.complexity_set.first(), type=type)
        df.at[type.id, 'raw_score'] = val.value
        df.at[type.id, 'weight'] = type.weight
        weighted_val = type.weight * val.value
        df.at[type.id, 'weighted_score'] = weighted_val
        raw_sum += val.value
        weighted_sum += weighted_val
    # Raw and weighted sums
    df.at['sum', 'raw_score'] = raw_sum
    df.at['sum', 'weighted_score'] = weighted_sum

    # Adjustment
    adjustment = 1.1
    if weighted_sum <= 25:
        adjustment = 1.1
    elif weighted_sum <= 50:
        adjustment = 1.15
    elif weighted_sum <= 75:
        adjustment = 1.2
    else:
        adjustment = 1.25
    df.at['adjustment', 'weighted_score'] = adjustment

    return df
