from clinical_effort.models import TrialArms, CTEffort, Cycles, CycleTypes

from ..serializers import TrialArmsSerializer

from .visits import add_visit

# Add cycle
def add_cycle(type, proj_id=None, arm_id=None):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)
    try:
        arm = TrialArms.objects.get(id=arm_id)
    except TrialArms.DoesNotExist:
        arm = None

    # Add cycle
    cycle_type = CycleTypes.objects.get(type=type)
    new_cycle = Cycles(instance=project, arm=arm, type=cycle_type, number_cycles=1, name=cycle_type.name)
    new_cycle.save()

    # Add visits for cycle
    add_visit(cycle_no=1, visit_no=1, cycle_id=new_cycle.id, proj_id=proj_id)

    return True

# Update cycle visit instances
def update_cycle(object, cycle_id=None, proj_id=None):

    # Retrieve cycle
    cycle = Cycles.objects.get(id=cycle_id)
    old_cycles = cycle.number_cycles
    old_visits = cycle.number_visits

    # Update cycle
    cycle.name = object['name']
    cycle.number_cycles = object['number_cycles']
    cycle.number_visits = object['number_visits']
    cycle.copy_hours = object['copy_hours']
    cycle.save()

    # Remove excess visits
    ex_cycles = cycle.visits_set.filter(cycle_number__gt=object['number_cycles']).delete()
    ex_visits = cycle.visits_set.filter(visit_number__gt=object['number_visits']).delete()

    # Get remaining visits
    visits = cycle.visits_set

    # Update visit count
    for i in range(1, object['number_cycles']+1):
        for j in range(1, object['number_visits']+1):

            # Get visit object
            if i > old_cycles or j > old_visits:
                add_visit(cycle_no=i, visit_no=j, cycle_id=cycle_id, proj_id=proj_id)

    # If copy hours checked, update visit values
    if object['copy_hours'] == True:
        visits = cycle.visits_set
        first_visit_value = cycle.visits_set.get(cycle_number=1, visit_number=1).value
        fields = cycle.

    return cycle
