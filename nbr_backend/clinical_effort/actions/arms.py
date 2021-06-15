from clinical_effort.models import TrialArms, TrialArmTypes, CTEffort, Cycles, CycleTypes, PersonnelFields

from .cycles import add_cycle
from .visits import add_value

# Add arm
def add_arm(name, cycle_names, type_id, proj_id=None):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)
    type = TrialArmTypes.objects.get(id=type_id)
    people = project.personnel_set.all()

    # Create arm
    arm = TrialArms(instance=project, name=name, type=type)
    arm.save()

    # Add initial field values
    for person in project.personnel_set.all():
        # Add default fields
        defaults = person.type.personneldefaults_set.all()
        for default in defaults:
            new_field = PersonnelFields(person=person, arm=arm, text=default.name)
            new_field.save()

    # Add cycles for arm
    for cycle in cycle_names:
        add_cycle(type=cycle, proj_id=proj_id, arm_id=arm.id)



    # # Add visit values
    # fields = person.personnelfields_set.all()
    # cycles = arm.cycles_set.all()
    # for cycle in cycles:
    #     visits = cycle.visits_set.all()
    #     for visit in visits:
    #         for field in fields:
    #             add_value(field, visit, 0)

    return True
