from django.conf import settings
import csv
from datetime import datetime
import pandas as pd

from clinical_effort.models import CTEffort
from clinical_effort.models import TrialArms
from clinical_effort.models import Personnel
from clinical_effort.models import PersonnelFields
from clinical_effort.models import VisitValues

# Get dataframe of person effort for an arm
def get_person_arm_df(proj_id, person_id, arm_id):

    # Get project
    project = CTEffort.objects.get(id=proj_id)
    person = Personnel.objects.get(id=person_id)
    arm = TrialArms.objects.get(id=arm_id)

    # Get complexity types
    cycles = arm.cycles_set.all()
    fields = PersonnelFields.objects.filter(person=person, arm=arm)

    # Dataframe
    # Assemble cols
    cols = ['item']
    index=[]
    i = 0
    for cycle in cycles:
        i += 1
        visits = cycle.visits_set.all()
        j = 0
        for visit in visits:
            j += 1
            cols.append(visit.id)
    for field in fields:
        index.append(field.id)
    index.append('sum')

    # Create df
    df = pd.DataFrame(index=index, columns=cols)

    # Initialize sum and cycle and visit headers
    for cycle in cycles:
        visits = cycle.visits_set.all()
        for visit in visits:
            df.at['sum', visit.id] = 0
    df.at['sum', 'item'] = 'Sum'

    for field in fields:
        df.at[field.id, 'item'] = field.text
        # row = {'item': field.text}
        for cycle in cycles:
            visits = cycle.visits_set.all()
            for visit in visits:
                # key = 'cycle_' + str(i) + '_visit_' + str(j)
                time = VisitValues.objects.get(field=field, visit=visit)
                # row[key] = time.value
                df.at[field.id, visit.id] = time.value
                df.at['sum', visit.id] = df.loc['sum', visit.id] + time.value
        # df = df.append(row, ignore_index=True)

    return df
