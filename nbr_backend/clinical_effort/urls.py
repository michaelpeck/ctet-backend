from rest_framework import routers
from .api import CTEffortViewSet, TrialArmsViewSet

router = routers.DefaultRouter()
router.register('api/effort', CTEffortViewSet, 'effort instances')
router.register('api/arms', TrialArmsViewSet, 'arms')

urlpatterns = router.urls
