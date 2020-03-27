from django.http import Http404
from rest_framework import status, permissions

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
#
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from rest_framework.response import Response

from rest_framework.views import APIView
from apply.serializers.basic import UserRegSerializer, UserDetailSerializer
from apply.utils.get_openid import OpenidUtils, verify

from apps.apply.models import UserProfile, EducationExperience, WorkExperience, Resume
from apps.apply.serializers import basic


class PermissionAPI(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request, *args, **kwargs):
        return Response({"1": 'ok'})


class UserLoginApi(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        code = request.data.get("js_code")
        openid = OpenidUtils(code)
        user=UserProfile.objects.filter(username=openid).first()
        if user is None:
            users = UserProfile.objects.create(username=openid)



        return Response({
            "code": 0,
            "data": openid
        })

    def post(self, request, *args, **kwargs):

        username = request.data['username']
        password = request.data['password']

        Account = UserProfile.objects.filter(username=username).first()
        if Account is None:
            users = UserProfile.objects.create_user(username=username, password=password)
            payload = jwt_payload_handler(users)
            token = jwt_encode_handler(payload)
        else:
            Account.set_password(password)
            Account.save()
            payload = jwt_payload_handler(Account)
            token = jwt_encode_handler(payload)
        return Response(status=status.HTTP_200_OK, data={'msg': '登陆成功', 'token': token})


class UserInfoApi(RetrieveUpdateAPIView):
    lookup_field = "username"
    queryset = UserProfile.objects.all()
    serializer_class = basic.UserDetailSerializer

    def get_serializer_class(self):
        if self.request.method == "PUT":

            return basic.UserRegSerializer
        else:
            return basic.UserDetailSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "code": 0,
            "data": serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):

            instance._prefetched_objects_cache = {}

        return Response({
            "code":0,
            "status":"修改成功",
            "data":serializer.data
        })







class EduExperienceApi(APIView):
    def get_object(self, pk):
        try:
            user = UserProfile.objects.get(username=pk)

            return EducationExperience.objects.filter(user_id=user.id)
        except EducationExperience.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        info = self.get_object(pk)
        serializer = basic.EduExperienceSerializer(info, many=True)
        return Response({
            "code": 0,
            "data": serializer.data
        })

    def post(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        data = request.data
        data["user"] = user.id
        serializer = basic.EduExperienceSerializer(data=data)
        return verify(serializer=serializer)

    def put(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        info = EducationExperience.objects.get(user_id=user.id, id=request.data.get("id"))

        serializer = basic.EduExperienceSerializer(info, data=request.data)
        return verify(serializer=serializer)

    def delete(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        info = EducationExperience.objects.get(user_id=user.id, id=request.data.get("id"))
        info.delete()
        return Response({
            "code": 0,
            "data": "删除成功"
        })


class WorkExperienceApi(APIView):
    """
    工作经历增删改查
    """

    def get_object(self, pk):
        try:
            user = UserProfile.objects.get(username=pk)

            return WorkExperience.objects.filter(user_id=user.id)
        except EducationExperience.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        info = self.get_object(pk)
        serializer = basic.WorkExperienceSerializer(info, many=True)
        return Response({
            "code": 0,
            "data": serializer.data
        })

    def post(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        data = request.data
        data["user"] = user.id
        serializer = basic.WorkExperienceSerializer(data=data)
        return verify(serializer=serializer)

    def put(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        info = WorkExperience.objects.get(user_id=user.id, id=request.data.get("id"))
        serializer = basic.WorkExperienceSerializer(info, data=request.data)
        return verify(serializer=serializer)

    def delete(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        info = WorkExperience.objects.get(user_id=user.id, id=request.data.get("id"))
        info.delete()
        return Response({
            "code": 0,
            "data": "删除成功"
        })


class ResumeApi(APIView):
    """
    简历自我描述及工作内容,填写以及修改
    """

    def get_object(self, pk):
        try:
            user = UserProfile.objects.get(username=pk)
            return Resume.objects.get(user_id=user.id)
        except Resume.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        info = self.get_object(pk)
        serializer = basic.ResumeInfoSerializer(info)
        return Response({
            "code": 0,
            "data": serializer.data
        })

    def post(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        data = request.data
        data["user"] = user.id
        res = Resume.objects.filter(user_id=user.id).exists()
        if res is True:
            info = self.get_object(pk)
            serializer = basic.ResumeInfoSerializer(info, data=request.data)
            return verify(serializer=serializer)
        else:
            serializer = basic.ResumeInfoSerializer(data=data)
            return verify(serializer=serializer)


class SkillApi(ListAPIView):


    def list(self, request, *args, **kwargs):
        openid=kwargs["pk"]
        user_obj=UserProfile.objects.filter(username=openid).first()
        infos=user_obj.applyinfo.position.skilllabel_set.all()
        data_list = list()
        for item in infos:
            data = dict()
            data['skill_name'] = item.skill_name

            data_list.append(data)
        return Response({
            "code":0,
            "data":data_list
        })

