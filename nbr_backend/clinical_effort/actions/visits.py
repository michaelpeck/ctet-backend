from clinical_effort.models import CTEffort, Cycles, Visits, VisitValue

# Add value
def add_value():

    return True


# Add visit
def add_visit(cycle_no, visit_no, proj_id=None, cycle_id=None):

    # Retrieve project and cycle
    project = CTEffort.objects.get(id=proj_id)
    cycle = Cycles.objects.get(id=cycle_id)

    # Add visit
    new_visit = Visits(instance=project, cycle=cycle, cycle_number=cycle_no, visit_number=visit_no)
    new_visit.save()

    # Add initial values
    for person in project.personnel_set.all():
        fields = person.personnelfields_set.all()
        for field in fields:
            new_val = VisitValue(field=field, visit=new_visit, value=0)
            new_val.save()


    return True
