from rest_framework import routers
from authentication import api
from django.urls import path
from .api import UserViewSet

# urlpatterns = [
#     path('user/',
#          api.get_user,
#          name = 'current-user'),
# ]

router = routers.DefaultRouter()
router.register('user', UserViewSet, 'current-user')

urlpatterns = router.urls
