from clinical_effort.models import CTEffort, Cycles, Visits, Years, YearValues

from .visits import add_value

# Add year
def add_year(proj_id):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)

    # Add year
    new_year = Years(instance=project)
    new_year.save()

    return new_year

# Add year value
def add_year_value(year, arm):

    # Add year
    new_value = YearValues(year=year, arm=arm)
    new_value.save()

    return new_value

# Add default years
def add_default_years(proj_id):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)

    # Add year
    year = add_year(proj_id)

    # Add people
    for arm in project.trialarms_set.all():
        add_year_value(year=year, arm=arm)

    return year
