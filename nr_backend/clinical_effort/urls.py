from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# from rest_framework import routers
#
#
# router = routers.DefaultRouter()
#
#
# urlpatterns = router.urls
