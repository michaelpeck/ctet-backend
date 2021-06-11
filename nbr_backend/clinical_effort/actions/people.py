from clinical_effort.models import CTEffort, Cycles, Visits, PersonnelTypes, Personnel, PersonnelFields, PersonnelDefaults

from .visits import add_value

# Add person
def add_person(proj_id, type_id, amount):

    # Retrieve project and cycle
    project = CTEffort.objects.get(id=proj_id)
    type = PersonnelTypes.objects.get(id=type_id)
    defaults = type.personneldefaults_set.all()
    cycles = project.cycles_set.all()

    # Add person
    new_person = Personnel(instance=project, type=type, name=type.name, amount=1)
    new_person.save()

    # Add default fields
    for default in defaults:
        new_field = PersonnelFields(instance=new_person, text=default.name)
        new_field.save()

    # Add visit values
    fields = new_person.personnelfields_set.all()
    for cycle in cycles:
        visits = cycle.visits_set.all()
        for visit in visits:
            for field in fields:
                add_value(field, visit, 0)

    return True

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
def add_field(project_id=None, person_id=None):

    # Retrieve person
    person = Personnel.objects.get(id=person_id)

    # Retrieve project
    project = CTEffort.objects.get(id=project_id)
    cycles = project.cycles_set.all()

    # Add field
    new_field = PersonnelFields(instance=person, text='New')
    new_field.save()

    # Add fields
    for cycle in cycles:
        visits = cycle.visits_set.all()
        for visit in visits:
            add_value(new_field, visit, 0)

    return True
