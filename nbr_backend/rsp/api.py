from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

import json
import io
import hashlib

from services.models import RspProj, RspProjComments, RspProjStatus, RspProjStatusLog, RspCommitteeStatusMap, User, Users, RspProjFile, RspUserProfile
from services.models import Node, ContentTypeProfile, RspReportEmailList, RspProjAffl, RspRoles, RspUserRole, RspProjFileCat
from .serializers import ProjectSerializer, ProjectCommentSerializer, StatusCommentSerializer, StatusLogSerializer, CommitteeStatusMapSerializer, RspUserProfileSerializer
from .serializers import UserProfileSerializer, UserRoleSerializer, NodeSerializer, SnapUsersSerializer, ReportEmailListSerializer, RspFileSerializer, ProjectAfflSerializer, RspRolesSerializer, RspFileCatSerializer
from .emails import piStatusEmail, piCommentEmail, ospApprovalEmail, committeeStatusEmail

# Project Viewset
class ProjectViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspProj.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'proj_id'

    @action(detail=False, methods=["GET"])
    def archived(self, request, proj_id=None):
        archived = RspProj.objects.filter(proj_archive=1)
        serializer = ProjectSerializer(archived, many=True)

        return Response(serializer.data, status=200)

    @action(detail=False, methods=["GET"])
    def completed(self, request, proj_id=None):
        completed = RspProjStatusLog.objects.filter(status_id__in = [6,7,8,11,13], status_type_id=8, status_current=1).values('proj_id')
        completed_projects = RspProj.objects.filter(proj_id__in = completed)
        serializer = ProjectSerializer(completed_projects, many=True)

        return Response(serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def project_affiliates(self, request, proj_id=None):
        affl = RspProjAffl.objects.filter(proj_id=proj_id)
        affl_serializer = ProjectAfflSerializer(affl, many=True)

        return Response(affl_serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def user(self, request, proj_id=None):
        user_projects = RspProj.objects.filter(drupal_uid=proj_id) # uid passed as proj_id in request
        serializer = ProjectSerializer(user_projects, many=True)
        return Response(serializer.data, status=200)

# Profile Viewset
class RspUserProfileViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspUserProfile.objects.all()
    serializer_class = RspUserProfileSerializer
    lookup_field = 'uid'


# Profile Viewset
class UserProfileViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = ContentTypeProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'vid'

    # get user profile by uid (uid is not a field in the content_type_profile table)
    @action(detail=True, methods=['GET'])
    def uid(self, request, vid=None):
        # get vid from uid via Node (in line below 'vid' is uid since that is the lookup key in the url)
        node = Node.objects.filter(type='profile', uid=vid)
        node_serializer = NodeSerializer(node[0], many=False)
        # get the profile instance from the vid
        instance = ContentTypeProfile.objects.filter(vid=node_serializer.data['vid'])
        serializer = UserProfileSerializer(instance[0], many=False)
        return Response(serializer.data, status=200)

# User Role Viewset
class UserRoleViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspUserRole.objects.all()
    serializer_class = UserRoleSerializer
    lookup_field = 'uid'


# SNAP Users Viewset
class SnapUsersViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Users.objects.all()
    serializer_class = SnapUsersSerializer
    lookup_field = 'uid'


# Project Comment Viewset
class ProjectCommentViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspProjComments.objects.all()
    serializer_class = ProjectCommentSerializer
    lookup_field = 'comment_id'

    @action(detail=False, methods=['POST'])
    def comment(self, request, comment_id=None):

        # Post comment
        comment_serializer = self.serializer_class(data=request.data)
        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save()

        # Get email recipients and send email notification
        affiliates = RspProjAffl.objects.filter(proj_id=request.data['proj_id'])
        affl_serializer = ProjectAfflSerializer(affiliates, many=True)
        to_email = []
        for affl in affl_serializer.data:
            to_email.append(affl['email'])
        subject = "RSP - New Comment"
        from_email = settings.EMAIL_HOST_USER
        to_email = ['michael.peck@nemours.org']
        print('emails', to_email) # remove when ready

        piCommentEmail(subject, from_email, to_email, comment_serializer.data)

        # Return
        return Response(comment_serializer.data, status=200)


    @action(detail=False, methods=['POST'])
    def get_project_comments(self, request, comment_id=None):
        print(request.data['proj_id'])
        # Comments from project comments table
        project_comments = RspProjComments.objects.filter(proj_id=request.data['proj_id'])
        pc_serializer = ProjectCommentSerializer(project_comments, many=True)
        # Comments from project status log table
        status_comments = RspProjStatusLog.objects.filter(proj_id=request.data['proj_id']).exclude(status_comment__isnull=True).exclude(status_comment__exact='')
        sc_serializer = StatusCommentSerializer(status_comments, many=True)
        # Combining all comments for a project
        send_data = pc_serializer.data + sc_serializer.data

        return Response(send_data, status=200)

    @action(detail=False, methods=['POST'])
    def get_user_comments(self, request, comment_id=None):
        # Get user projects
        projects = RspProj.objects.filter(drupal_uid=request.data['uid']).values('proj_id') # change to request.data['uid'] when ready (46 example)
        # Comments from project comments table
        project_comments = RspProjComments.objects.filter(proj_id__in=projects)
        pc_serializer = ProjectCommentSerializer(project_comments, many=True)
        # Comments from project status log table
        status_comments = RspProjStatusLog.objects.filter(proj_id__in=projects).exclude(status_comment__isnull=True).exclude(status_comment__exact='')
        sc_serializer = StatusCommentSerializer(status_comments, many=True)
        # Combining all comments for a project
        send_data = pc_serializer.data + sc_serializer.data

        return Response(send_data, status=200)



# Status Log Viewsets
class StatusLogViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspProjStatusLog.objects.all()
    serializer_class = StatusLogSerializer
    lookup_field = 'status_map_id'

    @action(detail=False, methods=['POST'])
    def get_history(self, request, status_map_id=None):

        history = RspProjStatusLog.objects.filter(proj_id=request.data['proj_id'])
        serializer = StatusLogSerializer(history, many=True)

        return Response(serializer.data, status=200)

    @action(detail=False, methods=['POST'])
    def get_user_history(self, request, status_map_id=None):
        # Get project IDs for all user projects
        projects = RspProj.objects.filter(drupal_uid=request.data['uid']).values('proj_id')
        # Get status log entries for those projects
        history = RspProjStatusLog.objects.filter(proj_id__in=projects)
        serializer = StatusLogSerializer(history, many=True)

        return Response(serializer.data, status=200)

    @action(detail=True, methods=['PUT', 'POST', 'GET'])
    def update_status(self, request, status_map_id=None):

        # Update previous status
        instance = self.queryset.get(status_map_id=status_map_id)
        serializer = self.serializer_class(instance, data={'status_current': 0}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Create new status
        serializer2 = StatusLogSerializer(data=request.data)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()

        # Get email recipients and send email notification
        affiliates = RspProjAffl.objects.filter(proj_id=request.data['proj_id'])
        affl_serializer = ProjectAfflSerializer(affiliates, many=True)
        to_email = []
        for affl in affl_serializer.data:
            to_email.append(affl['email'])
        subject = "RSP - Status Update"
        from_email = settings.EMAIL_HOST_USER
        to_email = ['michael.peck@nemours.org']
        print('emails', to_email) # remove when ready

        piStatusEmail(subject, from_email, to_email, serializer2.data)

        # If update status to "revision required", update overall status to "revision required"
        if serializer2.data['status_id'] == 18:
            # Update previous status
            overall_instance = self.queryset.get(proj_id=serializer2.data['proj_id'], status_type_id=8, status_current=1)
            overall_serializer = self.serializer_class(overall_instance, data={'status_current': 0}, partial=True)
            overall_serializer.is_valid(raise_exception=True)
            overall_serializer.save()

            # Create new status
            overall_data = request.data
            overall_data['status_type_id'] = 8
            overall_serializer2 = StatusLogSerializer(data=overall_data)
            overall_serializer2.is_valid(raise_exception=True)
            overall_serializer2.save()

        # If update status to "approved" or "waived", update status for next committee from "hold" to "needed"
        elif serializer2.data['status_id'] == 7 or serializer2.data['status_id'] == 21:
            print('status approved or waived')

            committee_map = [[13],[1],[5],[15,3,4,6,7],[16],[8]]
            next_step = False
            curr_index = 0
            for i in range(len(committee_map)):
                if serializer2.data['status_type_id'] in committee_map[i]:
                    print('status type in ', committee_map[i])
                    curr_index = i
                    same_order_stat = self.queryset.filter(proj_id=serializer2.data['proj_id'], status_current=1, status_type_id__in = committee_map[i], status_id__in = [7, 21])
                    if len(same_order_stat) == len(committee_map[i]):
                        next_step = True
                        print('next step is true')

            if next_step == True:
                for i in range(len(committee_map[curr_index+1])):
                    # Update previous status
                    next_instance = self.queryset.filter(proj_id=serializer2.data['proj_id'], status_type_id=committee_map[curr_index+1][i], status_current=1, status_id__in=[16])
                    print('next instance', next_instance[0])
                    if next_instance:
                        next_serializer = self.serializer_class(next_instance[0], data={'status_current': 0}, partial=True)
                        next_serializer.is_valid(raise_exception=True)
                        next_serializer.save()

                        # Create new status
                        next_data = request.data
                        next_data['status_type_id'] = committee_map[curr_index+1][i]
                        if committee_map[curr_index+1][i] == 16:
                            next_data['status_id'] = 2
                        else:
                            next_data['status_id'] = 14
                        next_serializer2 = StatusLogSerializer(data=next_data)
                        next_serializer2.is_valid(raise_exception=True)
                        next_serializer2.save()

                        # Email notification to committee
                        print('status type id', next_data['status_type_id'])
                        admins = RspRoles.objects.filter(status_type_id=next_data['status_type_id'], role_abbrev='adm')
                        print('admins', admins)
                        admin_serializer = RspRolesSerializer(admins, many=True)
                        to_email = []
                        for admn in admin_serializer.data:
                            to_email.append(admn['email'])
                        subject = "RSP - Status Update"
                        from_email = settings.EMAIL_HOST_USER
                        print('emails', to_email) # remove when ready
                        to_email = ['michael.peck@nemours.org']
                        print('emails', to_email) # remove when ready

                        committeeStatusEmail(subject, from_email, to_email, next_serializer2.data)

        # Check status for all required committees
        all_current = self.queryset.filter(proj_id=serializer2.data['proj_id'], status_current=1).exclude(status_type_id__in=[8])
        ready = False
        for i in all_current:
            if i.status_id == 2 and i.status_type_id == 16:
                subject = "RSP - Project Approval"
                from_email = settings.EMAIL_HOST_USER
                to_email = ['SponsoredProjectsDV@nemours.org', 'SponsoredProjectsNF@nemours.org', 'SponsoredProjectsCF@nemours.org']
                to_email = ['michael.peck@nemours.org']
                osp_project = RspProj.objects.filter(proj_id=serializer2.data['proj_id'])
                osp_serializer = ProjectSerializer(osp_project, many=False)
                osp_data = osp_serializer.data
                ospApprovalEmail(subject, from_email, to_email, osp_data)

            if i.status_id == 7 or i.status_id == 21:
                ready = False

        if ready == True:
            # Update previous status
            final_instance = self.queryset.get(proj_id=serializer2.data['proj_id'], status_type_id=8, status_current=1)
            final_serializer = self.serializer_class(final_instance, data={'status_current': 0}, partial=True)
            final_serializer.is_valid(raise_exception=True)
            final_serializer.save()

            # Create new status
            final_data = request.data
            final_data['status_type_id'] = 8
            final_data['status_id'] = 7
            final_serializer2 = StatusLogSerializer(data=final_data)
            final_serializer2.is_valid(raise_exception=True)
            final_serializer2.save()

        # Get updated project
        project = RspProj.objects.get(proj_id=request.data['proj_id'])
        serializer3 = ProjectSerializer(project, many=False)

        return Response(serializer3.data, status=200)

# Status Map Viewset
class StatusMapViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspCommitteeStatusMap.objects.all()
    serializer_class = CommitteeStatusMapSerializer
    lookup_field = 'committe_status_map_id'

# Report Email List Viewset
class ReportEmailListViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspReportEmailList.objects.all()
    serializer_class = ReportEmailListSerializer
    lookup_field = 'elid'

# File uploads
class RspFileUploadViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspProjFile.objects.all()
    serializer_class = RspFileSerializer
    lookup_field = 'file_id'

    @action(detail=True, methods=['GET'])
    def project_files(self, request, file_id=None):
        # Get file by project id (here file_id is project id so it can be placed in the url)
        files = RspProjFile.objects.filter(proj_id=file_id)
        serializer = RspFileSerializer(files, many=True)

        return Response(serializer.data, status=200)

    @action(detail=False, methods=['PUT', 'POST', 'GET'])
    def attachment(self, request, file_id=None):
        cat = RspProjFileCat.objects.filter(cat_id=request.data.get('file_cat')).values('cat_desc')
        if cat:
            category = cat[0]['cat_desc'] + ': '
        else:
            category = ''
        filelabel=category + request.data.get('file_label')
        filetkn=hashlib.md5(request.data.get('file_name').encode()).hexdigest()
        filename= 'reports/' + request.data.get('file_name')
        instance = RspProjFile(
                        media=request.FILES.get('attachment'),
                        proj_id=request.data.get('proj_id'),
                        file_cat=5,
                        file_committee=request.data.get('file_committee'),
                        file_name=filename,
                        file_label=filelabel,
                        file_tkn=filetkn,
                        drupal_uid=request.data.get('drupal_uid'),
                        file_archive=0,
                        file_date=request.data.get('status_change_date')
                        )
        instance.save()
        serializer = self.serializer_class(instance)
        print(serializer.data)
        return Response(serializer.data, status=200)

# Project Affiliate Viewset
class ProjectAffiliateViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = RspProjAffl.objects.all()
    serializer_class = ProjectAfflSerializer
    lookup_field = 'affl_id'

    @action(detail=False, methods=["POST"])
    def add(self, request, affl_id=None):

        affl_serializer = self.serializer_class(data=request.data)
        affl_serializer.is_valid(raise_exception=True)
        affl_serializer.save()

        return Response(affl_serializer.data, status=200)

    @action(detail=True, methods=["GET"])
    def delete(self, request, affl_id=None):

        try:
            instance = RspProjAffl.objects.filter(affl_id=affl_id)
            self.perform_destroy(instance[0])
        except Http404:
            pass

        return Response(affl_id, status=200)
