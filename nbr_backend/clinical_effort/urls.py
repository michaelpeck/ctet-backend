from rest_framework import routers
from .api import CTEffortViewSet, BaseCTEffortViewSet, TrialArmsViewSet, PersonnelViewSet, PersonnelFieldsViewSet, CyclesViewSet, ComplexityTypesViewSet, ComplexityValuesViewSet, VisitValuesViewSet, YearsViewSet, YearValuesViewSet

router = routers.DefaultRouter()
router.register('effort', CTEffortViewSet, 'effort instances')
router.register('projects', BaseCTEffortViewSet, 'base effort instances')
router.register('people', PersonnelViewSet, 'people')
router.register('fields', PersonnelFieldsViewSet, 'peorsonnel fields')
router.register('arms', TrialArmsViewSet, 'arms')
router.register('cycles', CyclesViewSet, 'cycles')
router.register('values', VisitValuesViewSet, 'values')
router.register('years', YearsViewSet, 'years')
router.register('year_values', YearValuesViewSet, 'year values')
router.register('complexity_types', ComplexityTypesViewSet, 'complexity types')
router.register('complexity_values', ComplexityValuesViewSet, 'complexity values')

urlpatterns = router.urls
