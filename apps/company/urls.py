from django.urls import path, re_path


from apps.company import views

urlpatterns = [

    re_path(r'hring/', views.HringCreateApi.as_view()),
    re_path(r'store/(?P<pk>\d+)/$', views.StoreAuthApi.as_view()),
    re_path(r'hringDetail/(?P<pk>\d+)/$', views.HringDetailApi.as_view()),


]