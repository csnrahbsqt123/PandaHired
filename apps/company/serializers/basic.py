from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# from PandaHired.settings import ALI_MEDIA_URL
from apps.apply import models


class PostHringDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CompanyHring
        fields="__all__"


class PostHringSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %X")
    job=serializers.CharField(source="job.job_name")
    class Meta:
        model=models.CompanyHring
        fields=("job_name","city","create_time","job","salary_range")
        extra_kwargs = {
            "job_name": {
                'read_only': True
            },
            'city': {
                'read_only': True
            },
        }



class StoreSerializer(serializers.ModelSerializer):
    # user=serializers.CharField(source="user.id")
    class Meta:
        model = models.StoreAuthentication
        fields = ("company_name",
                  "open_time",
                  "addr",
                  "shop_pic",
                  "business_licens",
                  "name",
                  "sex",
                  "birthday","entry_time","wx","phone","user"
                  )
