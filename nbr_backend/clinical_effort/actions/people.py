from clinical_effort.models import CTEffort, Cycles, Visits, PersonnelTypes, Personnel, PersonnelFields, PersonnelDefaults, TrialArms

from .visits import add_value

# Add person
def add_person(proj_id, type_id, amount):

    # Retrieve project and cycle
    project = CTEffort.objects.get(id=proj_id)
    type = PersonnelTypes.objects.get(id=type_id)
    cycles = project.cycles_set.all()

    # Add person
    new_person = Personnel(instance=project, type=type, name=type.name, amount=1)
    new_person.save()

    return new_person

# Add default people
def add_default_people(proj_id):

    # Retrieve project and personnel types
    project = CTEffort.objects.get(id=proj_id)
    types = PersonnelTypes.objects.all()

    # Add people
    for type in types:
        add_person(proj_id=proj_id, type_id=type.id, amount=1)

    return True


# Update cycle visit instances
def update_person(object, person_id=None, proj_id=None):

    # Retrieve person
    person = Personnel.objects.get(id=person_id)

    # Update person
    person.type = PersonnelTypes.objects.get(id=object['type'])
    person.amount = object['amount']
    person.save()


    return True


# Add field
def add_field(project_id=None, person_id=None, arm_id=None):

    # Retrieve person
    person = Personnel.objects.get(id=person_id)
    arm = TrialArms.objects.get(id=arm_id)

    # Retrieve project
    project = CTEffort.objects.get(id=project_id)
    cycles = project.cycles_set.filter(arm=arm_id)

    # Add field
    new_field = PersonnelFields(person=person, arm=arm, text='New')
    new_field.save()

    # Add fields
    for cycle in cycles:
        visits = cycle.visits_set.all()
        for visit in visits:
            add_value(new_field, visit, 0)

    return True


# Add person
def add_new_person_fields(proj_id, person):

    # Retrieve project and cycle
    project = CTEffort.objects.get(id=proj_id)
    arms = project.trialarms_set.all()

    for arm in arms:
        # Add default fields
        defaults = person.type.personneldefaults_set.all()
        for default in defaults:
            new_field = PersonnelFields(person=person, arm=arm, text=default.name)
            new_field.save()

    for arm in arms:
        for cycle in arm.cycles_set.all():
            for visit in cycle.visits_set.all():
                fields = PersonnelFields.objects.filter(arm=arm, person=person)
                for field in fields:
                    add_value(field, visit, 0)
    # Add visit values
    # fields = person.personnelfields_set.all()
    # cycles = arm.cycles_set.all()
    # for cycle in cycles:
    #     visits = cycle.visits_set.all()
    #     for visit in visits:
    #         for field in fields:
    #             add_value(field, visit, 0)


    return True
