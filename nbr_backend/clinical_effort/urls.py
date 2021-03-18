from rest_framework import routers
from .api import CTEffortViewSet, TrialArmsViewSet

router = routers.DefaultRouter()
router.register('effort', CTEffortViewSet, 'effort instances')
router.register('arms', TrialArmsViewSet, 'arms')

urlpatterns = router.urls
