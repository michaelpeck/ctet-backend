from clinical_effort.models import CTEffort, Cycles, Visits, VisitValues

# Add value
def add_value(field, visit, value):

    new_val = VisitValues(field=field, visit=visit, value=value)
    new_val.save()

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
        arm = cycle.arm
        fields = person.personnelfields_set.filter(arm=arm)
        for field in fields:
            new_val = VisitValues(field=field, visit=new_visit, value=0)
            new_val.save()


    return True


# Add person visit
# Add visit
def add_person_visit(cycle_no, visit_no, proj_id=None, cycle_id=None):

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
            new_val = VisitValues(field=field, visit=new_visit, value=0)
            new_val.save()


    return True
