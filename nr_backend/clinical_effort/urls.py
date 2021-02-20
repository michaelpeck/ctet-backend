from rest_framework import routers
from .api import CTEffortViewSet

router = routers.DefaultRouter()
router.register('api/effort-instances', CTEffortViewSet, 'effort instances')

urlpatterns = router.urls


# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#     path('', views.index, name='index'),
# ]
