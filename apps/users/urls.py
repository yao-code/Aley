from django.urls import path
from . import views

urlpatterns = [

    # 注册API
    path(r"register/", views.RegisterView.as_view(), name="register"),

    # 获取验证码API
    path(r"captcha/", views.CaptchaView.as_view(), name="captcha"),

    # 登陆API
    path(r"login/", views.LoginView.as_view(), name="login"),

    
]