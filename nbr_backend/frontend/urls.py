
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index),
    re_path('bric', views.index),
    re_path('requests', views.index),
    re_path('request-submitted', views.index),
]
