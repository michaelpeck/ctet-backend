from rest_framework import serializers
from services.models import RspProj, RspProjComments, RspProjStatus, RspProjStatusLog, RspStatusType, RspCommitteeStatusMap, RspProjFile, Realname, User, Users, Files, RspReportEmailList
from services.models import ContentTypeProfile, Node, RspProjAffl, RspRoles, RspUserRole, RspProjFileCat, RspUserProfile

# Load Serializers
class ProjectSerializer(serializers.ModelSerializer):

    completed = serializers.SerializerMethodField()
    nbr = serializers.SerializerMethodField()
    crrc = serializers.SerializerMethodField()
    radiation = serializers.SerializerMethodField()
    ibc = serializers.SerializerMethodField()
    iacuc = serializers.SerializerMethodField()
    hsrss = serializers.SerializerMethodField()
    irb = serializers.SerializerMethodField()
    bmc_irc = serializers.SerializerMethodField()
    osp = serializers.SerializerMethodField()
    overall_status = serializers.SerializerMethodField()


    class Meta:
        model = RspProj
        fields = '__all__'

    def get_completed(self, obj):
        completed = RspProjStatusLog.objects.filter(status_id__in = [6,7,8,11,13], status_type_id=8, status_current=1, proj_id=obj.proj_id)
        if (completed):
            return 1
        else:
            return 0

    def get_nbr(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=13, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [13, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [13, '', '', '']

    def get_crrc(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=1, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [1, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [1, '', '', '']

    def get_radiation(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=15, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [15, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [15, '', '', '']

    def get_ibc(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=3, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [3, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [3, '', '', '']

    def get_iacuc(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=4, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [4, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [4, '', '', '']

    def get_hsrss(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=5, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [5, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [5, '', '', '']

    def get_irb(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=6, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [6, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [6, '', '', '']

    def get_bmc_irc(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=7, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [7, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [7, '', '', '']

    def get_osp(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=16, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [16, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc']]
        else:
            return [16, '', '', '']

    def get_overall_status(self, obj):
        qry = RspProjStatusLog.objects.filter(status_type_id=8, status_current=1, proj_id=obj.proj_id).values('status_id', 'status_map_id', 'status_change_date')
        if qry:
            status = RspProjStatus.objects.filter(status_id=qry[0]['status_id']).values('status_desc')
            return [8, qry[0]['status_map_id'], qry[0]['status_id'], status[0]['status_desc'], qry[0]['status_change_date']]
        else:
            return [8, '', '', '', '']


class ProjectCommentSerializer(serializers.ModelSerializer):

    proj_identifier = serializers.SerializerMethodField()
    created_by_user = serializers.SerializerMethodField()
    committee = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = RspProjComments
        fields = '__all__'

    def get_proj_identifier(self, obj):
        ident = RspProj.objects.filter(proj_id=obj.proj_id).values('proj_identifier')
        if ident:
            return ident[0]['proj_identifier']
        else:
            return ''

    def get_created_by_user(self, obj):
        name = Realname.objects.filter(uid=obj.created_by).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''

    def get_committee(self, obj):
        stat = RspStatusType.objects.filter(status_type_id=obj.committee_id).values('status_type_name')
        if stat:
            return stat[0]['status_type_name']
        else:
            return ''

    def get_status(self, obj):
        stat = RspProjStatus.objects.filter(status_id=obj.status_id).values('status_desc')
        if stat:
            return stat[0]['status_desc']
        else:
            return ''

class StatusCommentSerializer(serializers.ModelSerializer):

    proj_identifier = serializers.SerializerMethodField()
    committee_id = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    posted_date = serializers.SerializerMethodField()

    created_by_user = serializers.SerializerMethodField()
    committee = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = RspProjStatusLog
        fields = ('proj_id', 'proj_identifier', 'committee_id', 'committee', 'status_id', 'status', 'comment', 'status_map_id', 'created_by', 'created_by_user', 'posted_date', 'modified_date')

    def get_proj_identifier(self, obj):
        ident = RspProj.objects.filter(proj_id=obj.proj_id).values('proj_identifier')
        if ident:
            return ident[0]['proj_identifier']
        else:
            return ''

    def get_committee_id(self, obj):
        id = obj.status_type_id
        if id:
            return id
        else:
            return ''

    def get_comment(self, obj):
        id = obj.status_comment
        if id:
            return id
        else:
            return ''

    def get_created_by(self, obj):
        id = obj.modified_by
        if id:
            return id
        else:
            return ''
    def get_posted_date(self, obj):
        id = obj.status_change_date
        if id:
            return id
        else:
            return ''

    def get_created_by_user(self, obj):
        name = Realname.objects.filter(uid=obj.modified_by).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''

    def get_committee(self, obj):
        stat = RspStatusType.objects.filter(status_type_id=obj.status_type_id).values('status_type_name')
        if stat:
            return stat[0]['status_type_name']
        else:
            return ''

    def get_status(self, obj):
        stat = RspProjStatus.objects.filter(status_id=obj.status_id).values('status_desc')
        if stat:
            return stat[0]['status_desc']
        else:
            return ''


class StatusLogSerializer(serializers.ModelSerializer):

    proj_identifier = serializers.SerializerMethodField()
    proj_title = serializers.SerializerMethodField()
    pi_name = serializers.SerializerMethodField()
    status_type = serializers.SerializerMethodField()
    status_type_slug = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    attachment = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    modified_by_user = serializers.SerializerMethodField()


    class Meta:
        model = RspProjStatusLog
        fields = '__all__'

    def get_proj_identifier(self, obj):
        proj = RspProj.objects.filter(proj_id=obj.proj_id).values('proj_identifier')
        if proj:
            return proj[0]['proj_identifier']
        else:
            return ''

    def get_proj_title(self, obj):
        proj = RspProj.objects.filter(proj_id=obj.proj_id).values('proj_title')
        if proj:
            return proj[0]['proj_title']
        else:
            return ''

    def get_pi_name(self, obj):
        proj = RspProj.objects.filter(proj_id=obj.proj_id).values('proj_first_name', 'proj_last_name')
        if proj:
            name = proj[0]['proj_last_name'] + ', ' + proj[0]['proj_first_name']
            return name
        else:
            return ''

    def get_status_type(self, obj):
        stat = RspStatusType.objects.filter(status_type_id=obj.status_type_id).values('status_type_name')
        if stat:
            return stat[0]['status_type_name']
        else:
            return ''

    def get_status(self, obj):
        stat = RspProjStatus.objects.filter(status_id=obj.status_id).values('status_desc')
        if stat:
            return stat[0]['status_desc']
        else:
            return ''

    def get_attachment(self, obj):
        qry = RspProjFile.objects.filter(file_id=obj.file_id).values('file_name', 'file_label', 'file_tkn')
        if qry:
            return qry[0]['file_name']
        else:
            return ''

    def get_file(self, obj):
        qry = RspProjFile.objects.filter(file_id=obj.file_id).values('file_name', 'file_label', 'file_tkn')
        # file = open('669_comm_20170822130200_00153.pdf', 'r')

        if qry:
            return qry
        else:
            return ''

    def get_status_type_slug(self, obj):
        slugs = ['', 'crrc', '', 'ibc', 'iacuc', 'hsrss', 'irb', 'bmc_irc', 'overall_status', '', '', '', '', 'nbr', '', 'radiation', 'osp']
        index = obj.status_type_id
        if index:
            return slugs[index]
        else:
            return ''

    def get_modified_by_user(self, obj):
        name = Realname.objects.filter(uid=obj.modified_by).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''


class CommitteeStatusMapSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField()
    next_status = serializers.SerializerMethodField()

    class Meta:
        model = RspCommitteeStatusMap
        fields = '__all__'

    def get_current_status(self, obj):
        stat = RspProjStatus.objects.filter(status_id=obj.current_status_id).values('status_desc')
        if stat:
            return stat[0]['status_desc']
        else:
            return ''

    def get_next_status(self, obj):
        stat = RspProjStatus.objects.filter(status_id=obj.next_status_id).values('status_desc')
        if stat:
            return stat[0]['status_desc']
        else:
            return ''


class RspUserProfileSerializer(serializers.ModelSerializer):

    cv_filepath = serializers.SerializerMethodField()
    biosketch_filepath = serializers.SerializerMethodField()

    class Meta:
        model = RspUserProfile
        fields = '__all__'


    def get_cv_filepath(self, obj):
        file = Files.objects.filter(fid=obj.cv).values('filepath')
        if file:
            return file[0]['filepath']
        else:
            return ''

    def get_biosketch_filepath(self, obj):
        file = Files.objects.filter(fid=obj.biosketch).values('filepath')
        if file:
            return file[0]['filepath']
        else:
            return ''


class UserProfileSerializer(serializers.ModelSerializer):

    uid = serializers.SerializerMethodField()
    cv_filepath = serializers.SerializerMethodField()
    biosketch_filepath = serializers.SerializerMethodField()

    class Meta:
        model = ContentTypeProfile
        fields = '__all__'

    def get_uid(self, obj):
        node_uid = Node.objects.filter(vid=obj.vid).values('uid')
        if node_uid:
            return node_uid[0]['uid']
        else:
            return ''

    def get_cv_filepath(self, obj):
        file = Files.objects.filter(fid=obj.field_profile_cv_fid).values('filepath')
        if file:
            return file[0]['filepath']
        else:
            return ''

    def get_biosketch_filepath(self, obj):
        file = Files.objects.filter(fid=obj.field_profile_biosketch_fid).values('filepath')
        if file:
            return file[0]['filepath']
        else:
            return ''

class UserRoleSerializer(serializers.ModelSerializer):

    role_name = serializers.SerializerMethodField()
    role_abbrev = serializers.SerializerMethodField()
    committee = serializers.SerializerMethodField()
    status_type_id = serializers.SerializerMethodField()

    class Meta:
        model = RspUserRole
        fields = '__all__'

    def get_role_name(self, obj):
        role_id = RspRoles.objects.filter(rsp_role_id=obj.rsp_role_id).values('role_name')
        if role_id:
            return role_id[0]['role_name']
        else:
            return ''

    def get_role_abbrev(self, obj):
        role_id = RspRoles.objects.filter(rsp_role_id=obj.rsp_role_id).values('role_abbrev')
        if role_id:
            return role_id[0]['role_abbrev']
        else:
            return ''

    def get_committee(self, obj):
        role_id = RspRoles.objects.filter(rsp_role_id=obj.rsp_role_id).values('committee')
        if role_id:
            return role_id[0]['committee']
        else:
            return ''

    def get_status_type_id(self, obj):
        role_id = RspRoles.objects.filter(rsp_role_id=obj.rsp_role_id).values('status_type_id')
        if role_id:
            return role_id[0]['status_type_id']
        else:
            return ''


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = '__all__'

class SnapUsersSerializer(serializers.ModelSerializer):

    realname = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ('uid', 'name', 'mail', 'is_admin', 'realname')

    def get_realname(self, obj):
        name = Realname.objects.filter(uid=obj.uid).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''

class ReportEmailListSerializer(serializers.ModelSerializer):

    realname = serializers.SerializerMethodField()

    class Meta:
        model = RspReportEmailList
        fields = '__all__'

    def get_realname(self, obj):
        name = Realname.objects.filter(uid=obj.uid).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''

class RspFileSerializer(serializers.ModelSerializer):

    committee = serializers.SerializerMethodField()
    realname = serializers.SerializerMethodField()

    class Meta:
        model = RspProjFile
        fields = '__all__'

    def get_committee(self, obj):
        comm = RspStatusType.objects.filter(status_type_id=obj.file_committee).values('status_type_name')
        if comm:
            return comm[0]['status_type_name']
        else:
            return ''

    def get_realname(self, obj):
        name = Realname.objects.filter(uid=obj.drupal_uid).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''

class RspFileCatSerializer(serializers.ModelSerializer):

    class Meta:
        model = RspProjFileCat
        fields = '__all__'


class ProjectAfflSerializer(serializers.ModelSerializer):

    realname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = RspProjAffl
        fields = '__all__'

    def get_realname(self, obj):
        name = Realname.objects.filter(uid=obj.drupal_uid).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''

    def get_email(self, obj):
        email = Users.objects.filter(uid=obj.drupal_uid).values('mail')
        if email:
            return email[0]['mail']
        else:
            return ''


class RspRolesSerializer(serializers.ModelSerializer):

    uid = serializers.SerializerMethodField()
    realname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = RspRoles
        fields = '__all__'

    def get_uid(self, obj):
        uid = RspUserRole.objects.filter(rsp_role_id=obj.rsp_role_id).values('uid')
        if uid:
            return uid[0]['uid']
        else:
            return ''

    def get_realname(self, obj):
        uid_obj = RspUserRole.objects.filter(rsp_role_id=obj.rsp_role_id).values('uid')
        uid = ''
        name = ''
        if uid_obj:
            uid = uid_obj[0]['uid']
            name = Realname.objects.filter(uid=uid).values('realname')
        if name:
            return name[0]['realname']
        else:
            return ''

    def get_email(self, obj):
        uid_obj = RspUserRole.objects.filter(rsp_role_id=obj.rsp_role_id).values('uid')
        uid = ''
        email = ''
        if uid_obj:
            uid = uid_obj[0]['uid']
            email = Users.objects.filter(uid=uid).values('mail')
        if email:
            return email[0]['mail']
        else:
            return ''
