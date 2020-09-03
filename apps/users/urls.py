from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path(r"register/", views.RegisterView.as_view(), name="register"),
    path(r"captcha/", views.CaptchaView.as_view(), name="captcha"),
]