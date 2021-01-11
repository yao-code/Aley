from django.urls import path
from django.urls import re_path
from . import views
from rest_framework.generics import ListCreateAPIView
from ..users.models import User
from ..users.serializers import UserSerializer

urlpatterns = [
    # 视图重试
    path(r"test1/", views.Test_1.as_view()),
    path(r"test2/", views.Test_2.as_view()),
    path(r"test3/", views.Test_3.as_view()),
    path(r"test4/", views.Test_4.as_view()),
    path(r"test5/", views.Test_5.as_view()),
    path(r"test6/", views.Test_6.as_view()),
    path(r"test7/", views.Test_7.as_view()),
    path(r"test8/", views.Test_8.as_view()),
    path(r"test9/", views.Test_9.as_view()),

    # request 解析
    path(r"data/", views.Data.as_view()),
    path(r"query_params/", views.QueryParams.as_view()),
    path(r"parsers/", views.Parsers.as_view()),

    # 响应
    path(r"test_response/", views.TestResponse.as_view()),

    # 通用视图
    path(r"userlist/", views.UserList.as_view()),
    path(r'userlist1/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer),
         name='user-list'),
    path(r"userlist2/", views.UserList2.as_view()),
    re_path(r"^userlist2/(?P<uid>\d+)/$", views.UserList2.as_view()),

]
