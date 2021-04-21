from clinical_effort.models import CTEffort, Cycles, Visits, CRCVisit, NCVisit, DCVisit, GeneralVisit

from ..serializers import TrialArmsSerializer

# Add visit
def add_visit(cycle_no, visit_no, proj_id=None, cycle_id=None):

    # Retrieve project and cycle
    project = CTEffort.objects.get(id=proj_id)
    cycle = Cycles.objects.get(id=cycle_id)

    # Add visit
    new_visit = Visits(instance=project, cycle=cycle, cycle_number=cycle_no, visit_number=visit_no)
    new_visit.save()

    # Add visit types
    crc_visit = CRCVisit(visit=new_visit)
    nc_visit = NCVisit(visit=new_visit)
    dc_visit = DCVisit(visit=new_visit)
    g_visit = GeneralVisit(visit=new_visit)

    return True
