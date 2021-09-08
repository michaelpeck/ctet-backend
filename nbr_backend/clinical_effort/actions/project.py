from clinical_effort.models import CTEffort, CycleTypes, Cycles
from ..serializers import CTEffortSerializer


from .arms import add_arm
from .people import add_default_people
from .years import add_default_years

# Create new project
def setup_project(object, id=None):

    # Get project
    project = CTEffort.objects.get(id=id)

    # Add eid

    # Add people
    add_default_people(id)

    # Create project pre cycles
    pre_cycles = ['pre-screening', 'screening']
    add_arm(name='Screening', cycle_names=pre_cycles, type_id=1, proj_id=id)

    # Create 1 arm
    arm_cycles = ['standard', 'custom']
    add_arm(name='Arm 1', cycle_names=arm_cycles, type_id=2, proj_id=id)

    # Create project post cycles
    post_cycles = ['end-of-treatment', 'follow-up']
    add_arm(name='Follow-up', cycle_names=post_cycles, type_id=3, proj_id=id)

    # Add years
    add_default_years(id)


    project = CTEffort.objects.get(id=id)
    serializer = CTEffortSerializer(project, many=False)


# Update all project cycles
# def update_cycles(object, id=None):

# Create project eid ('CTET[YY]-[user]-[#userproject]')
def create_project_eid(project):

    # Get user

    # Get year
    return
