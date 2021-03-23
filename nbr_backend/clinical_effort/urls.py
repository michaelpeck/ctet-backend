from rest_framework import routers
from .api import CTEffortViewSet, TrialArmsViewSet, CyclesViewSet

router = routers.DefaultRouter()
router.register('effort', CTEffortViewSet, 'effort instances')
router.register('arms', TrialArmsViewSet, 'arms')
router.register('cycles', CyclesViewSet, 'cycles')

urlpatterns = router.urls
