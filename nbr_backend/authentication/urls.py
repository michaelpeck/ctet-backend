from rest_framework import routers
from authentication import api
from django.urls import path

import authentication.api as v

router = routers.DefaultRouter()
router.register('user', v.UserViewSet, 'current-user')
router.register('users', v.UsersViewSet, 'users')
router.register('user_profiles', v.UserProfilesViewSet, 'user-profiles')

urlpatterns = router.urls
