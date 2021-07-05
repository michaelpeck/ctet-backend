
from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index),
    re_path('effort', views.index),
    re_path('effort/', views.index),
    re_path('projects', views.index),
    re_path('projects/', views.index),
    re_path('profile', views.index),
    re_path('profile/', views.index),
]
