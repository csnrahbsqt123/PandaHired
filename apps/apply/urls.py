from django.urls import path, re_path

from rest_framework_jwt.views import obtain_jwt_token

from apply import views

urlpatterns = [

    # path('login/', obtain_jwt_token),
    re_path(r'userInfo/(?P<username>\d+)/$', views.UserInfoApi.as_view(),name="个人信息"),
    # re_path(r'applyInfo/(?P<pk>\d+)/$', views.ApplyInfoApi.as_view(),name="求职者意向"),
    re_path(r'education/(?P<pk>\d+)/$', views.EduExperienceApi.as_view()),
    re_path(r'work/(?P<pk>\d+)/$', views.WorkExperienceApi.as_view()),
    re_path(r'resume/(?P<pk>\d+)/$', views.ResumeApi.as_view()),
    re_path(r'skill/(?P<pk>\d+)/$', views.SkillApi.as_view()),
    re_path(r'permission/$', views.PermissionAPI.as_view()),

    re_path(r'login/$', views.UserLoginApi.as_view(),name="用户登录"),
]