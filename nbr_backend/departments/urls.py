from rest_framework import routers
from .api import SupportRequestViewSet

router = routers.DefaultRouter()
router.register('support-request', SupportRequestViewSet, 'support requests')

urlpatterns = router.urls
