import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# from PandaHired.settings import ALI_MEDIA_URL
from apply.utils.get_openid import work_time
from apps.apply import models


class PositionSerializer(serializers.ModelSerializer):
    # job_type = serializers.CharField(source="j.job_type")
    class Meta:
        model = models.Position
        fields = "__all__"




class UserDetailSerializer(serializers.ModelSerializer):
    # year = serializers.SerializerMethodField()
    # def get_year(self, instance):
    #     entry_time = instance.entry_time
    #     if entry_time is not None:
    #         return work_time(datetime.datetime.strftime(entry_time, "%Y-%m-%d"))
    #     return ""
    class Meta:
        model = models.UserProfile
        fields = "__all__"


class UserRegSerializer(serializers.ModelSerializer):

    # head = serializers.SerializerMethodField()

    # pro_certificate = serializers.SerializerMethodField()
    # id_verify = serializers.SerializerMethodField()

    # def create(self, validated_data):
    #     user = super(UserSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # def validate(self, attrs):
    #     import re
    #     phone=attrs.get("phone")
    #     pattern = re.compile('^1[3-9]\d{9}')
    #
    #     if not pattern.match(phone):
    #         raise serializers.ValidationError("手机格式错误")

    # def get_head(self, instance):
    #     head = instance.head
    #     return ALI_MEDIA_URL + str(head)

    class Meta:
        model = models.UserProfile
        fields = "__all__"


class EduExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EducationExperience
        fields = "__all__"


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkExperience
        fields = "__all__"

class ResumeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Resume
        fields = "__all__"


class SkillLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SkillLabel
        fields="__all__"


