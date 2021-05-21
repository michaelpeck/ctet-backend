from clinical_effort.models import CTEffort, CycleTypes, Cycles
from ..serializers import CTEffortSerializer


from .arms import add_arm
from .cycles import add_cycle
from .person import add_default_people

# Create new project
def setup_project(object, id=None):

    # Get project
    project = CTEffort.objects.get(id=id)

    # Add people
    add_default_people(id)

    # Create project pre cycles
    pre_cycles = ['pre-screening', 'screening']
    for cycle in pre_cycles:
        add_cycle(type=cycle, proj_id=id)

    # Create 1 arm
    add_arm(name='Arm 1', proj_id=id)

    # Create project post cycles
    post_cycles = ['end-of-treatment', 'follow-up']
    for cycle in post_cycles:
        add_cycle(type=cycle, proj_id=id)

    project = CTEffort.objects.get(id=id)
    serializer = CTEffortSerializer(project, many=False)


# Update all project cycles
# def update_cycles(object, id=None):
