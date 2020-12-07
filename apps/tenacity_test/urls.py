from django.urls import path
from . import views


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
]