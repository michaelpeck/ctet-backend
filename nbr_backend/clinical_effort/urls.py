from rest_framework import routers
from .api import CTEffortViewSet, TrialArmsViewSet, PersonnelViewSet, PersonnelFieldsViewSet, CyclesViewSet, ComplexityTypesViewSet

router = routers.DefaultRouter()
router.register('effort', CTEffortViewSet, 'effort instances')
router.register('people', PersonnelViewSet, 'people')
router.register('fields', PersonnelFieldsViewSet, 'peorsonnel fields')
router.register('arms', TrialArmsViewSet, 'arms')
router.register('cycles', CyclesViewSet, 'cycles')
router.register('complexity_types', ComplexityTypesViewSet, 'complexity types')

urlpatterns = router.urls
