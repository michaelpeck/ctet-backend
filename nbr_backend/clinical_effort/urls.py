from rest_framework import routers
import clinical_effort.api as v

router = routers.DefaultRouter()
router.register('effort', v.CTEffortViewSet, 'effort instances')
router.register('projects', v.BaseCTEffortViewSet, 'base effort instances')
router.register('access', v.ProjectAccessViewSet, 'project access relationships')
router.register('access_types', v.ProjectAccessTypesViewSet, 'project access types')
router.register('people', v.PersonnelViewSet, 'people')
router.register('fields', v.PersonnelFieldsViewSet, 'peorsonnel fields')
router.register('arms', v.TrialArmsViewSet, 'arms')
router.register('cycles', v.CyclesViewSet, 'cycles')
router.register('values', v.VisitValuesViewSet, 'values')
router.register('years', v.YearsViewSet, 'years')
router.register('notes', v.NotesViewSet, 'notes')
router.register('year_values', v.YearValuesViewSet, 'year values')
router.register('complexity_types', v.ComplexityTypesViewSet, 'complexity types')
router.register('complexity_values', v.ComplexityValuesViewSet, 'complexity values')

urlpatterns = router.urls
