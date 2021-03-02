from rest_framework import routers
from .api import SupportRequestViewSet

router = routers.DefaultRouter()
router.register('api/support-request', SupportRequestViewSet, 'support requests')

urlpatterns = router.urls
