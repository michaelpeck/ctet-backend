from clinical_effort.models import CTEffort, Cycles, Visits, SummaryYears

from .visits import add_value

# Add year
def add_year(proj_id, number):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)

    # Add year
    new_year = SummaryYears(instance=project, number=number)
    new_year.save()

    return True

# Add default years
def add_default_years(proj_id):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)

    # Add people
    for i in range(1, 10):
        add_year(proj_id=proj_id, number=i)

    return True
