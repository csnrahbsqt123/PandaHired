import django_filters
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import pagination, filters, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, \
    RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.apply import models
from apps.apply.models import UserProfile, CompanyHring, StoreAuthentication
from apps.apply.utils.get_openid import verify

from apps.company.serializers import basic

from apps.company.serializers.basic import PostHringSerializer, StoreSerializer


class HringFilter(django_filters.rest_framework.FilterSet):
    """职位过滤类"""

    city = django_filters.CharFilter(field_name="city", )
    job = django_filters.CharFilter(field_name="job", )
    salary_range = django_filters.CharFilter(field_name="salary_range", )
    job_name = django_filters.CharFilter(field_name="job_name",lookup_expr="icontains")  # icontains 表示 包含（忽略大小写）

    class Meta:
        model = models.CompanyHring  # 关联的表
        fields = ["city","job_name","job","salary_range"]  # 过滤的字段




class HringCreateApi(ListCreateAPIView):
    queryset = models.CompanyHring.objects.all()
    serializer_class = basic.PostHringSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({
            "code": 1,
            "errors": serializer.errors
        })

        # 过滤器

    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filter_class=HringFilter

    # search_fields = ("job_name", "city")
    ordering_fields = ("create_time",)
    # 分页器
    pagination_class = pagination.LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 帮助实现分页的代码
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "code": 0,
            "data": {

                "table_data": serializer.data
            }
        })

    def get_paginated_response(self, data):
        ordering = self.request.query_params.get("ordering", "")
        reverse = False
        if ordering:
            if ordering.startswith("-"):
                reverse = True
                ordering = ordering[1:]
            data.sort(key=lambda item: item[ordering], reverse=reverse)
        return Response({
            "code": 0,
            "data": {

                "table_data": {
                    "total": self.paginator.count,
                    "data": data
                }
            }
        })


class HringDetailApi(RetrieveUpdateAPIView):
    queryset = models.CompanyHring.objects.all()
    serializer_class = basic.PostHringDetailSerializer

    def get_serializer_class(self):
        if self.request.method == "PUT":

            return basic.PostHringSerializer
        else:
            return basic.PostHringDetailSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)





class StoreAuthApi(APIView):
    def get_object(self, pk):
        try:
            user = UserProfile.objects.get(username=pk)
            return StoreAuthentication.objects.get(user_id=user.id)
        except StoreAuthentication.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        info = self.get_object(pk)
        serializer = StoreSerializer(info)
        return Response({
            "code": 0,
            "data": serializer.data
        })

    def post(self, request, pk, format=None):
        user = UserProfile.objects.get(username=pk)
        data = request.data
        data["user"] = user.id

        serializer = StoreSerializer(data=data)
        return verify(serializer=serializer)
