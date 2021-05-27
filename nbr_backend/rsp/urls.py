from rest_framework import routers
from .api import ProjectViewSet, ProjectCommentViewSet, StatusMapViewSet, StatusLogViewSet, UserProfileViewSet, RspUserProfileViewSet, UserRoleViewSet, SnapUsersViewSet, ReportEmailListViewSet, RspFileUploadViewSet, ProjectAffiliateViewSet

router = routers.DefaultRouter()
router.register('api/services', ProjectViewSet, 'projects')
router.register('api/comments', ProjectCommentViewSet, 'comment')
router.register('api/statusmap', StatusMapViewSet, 'status map')
router.register('api/status', StatusLogViewSet, 'status log')
router.register('api/statushistory', StatusLogViewSet, 'status history')
router.register('api/user', UserProfileViewSet, 'user profile')
router.register('api/user_p', RspUserProfileViewSet, 'new user profile')
router.register('api/user_role', UserRoleViewSet, 'user role')
router.register('api/users_snap', SnapUsersViewSet, 'user list')
router.register('api/report_email_list', ReportEmailListViewSet, 'report email list')
router.register('api/rsp_files', RspFileUploadViewSet, 'file uploads')
router.register('api/affiliates', ProjectAffiliateViewSet, 'project affiliates')

urlpatterns = router.urls
