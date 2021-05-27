from rest_framework import routers
from .api import CTEffortViewSet, TrialArmsViewSet, PersonnelViewSet, CyclesViewSet, ComplexityTypesViewSet

router = routers.DefaultRouter()
router.register('effort', CTEffortViewSet, 'effort instances')
router.register('people', PersonnelViewSet, 'people')
router.register('arms', TrialArmsViewSet, 'arms')
router.register('cycles', CyclesViewSet, 'cycles')
router.register('complexity_types', ComplexityTypesViewSet, 'complexity types')

urlpatterns = router.urls
