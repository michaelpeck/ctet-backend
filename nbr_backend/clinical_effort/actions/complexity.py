from clinical_effort.models import CTEffort, Cycles, CycleTypes, ComplexityTypes, Complexity, ComplexityValues



# Add cycle
def create_complexity(proj_id=None):

    # Retrieve project
    project = CTEffort.objects.get(id=proj_id)

    # Add complexity
    new_complexity = Complexity(instance=project)
    new_complexity.save()

    # Add complexity
    types = ComplexityTypes.objects.all()
    for type in types:
        new_val = ComplexityValues(complexity=new_complexity, type=type)
        new_val.save()

    return True
