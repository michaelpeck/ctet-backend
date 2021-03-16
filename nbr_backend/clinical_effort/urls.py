from rest_framework import routers
from .api import CTEffortViewSet

router = routers.DefaultRouter()
router.register('api/effort', CTEffortViewSet, 'Effort Instances')

urlpatterns = router.urls
