from clinical_effort.models import TrialArms, CTEffort, Cycles, CycleTypes

from ..serializers import TrialArmsSerializer

from .cycles import add_cycle

# Add arm
def add_arm(name, proj_id=None):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)

    # Create arm
    arm = TrialArms(instance=project, name=name)
    arm.save()

    # Add cycles for arm
    arm_cycles = ['standard', 'custom']
    for cycle in arm_cycles:
        add_cycle(type=cycle, proj_id=proj_id, arm_id=arm.id)

    return True
