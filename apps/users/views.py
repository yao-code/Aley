from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from . import forms
from .models import User
from .serializers import UserSerializer
from utils.response import MyResponse


# Create your views here.

def index(request):
    return JsonResponse({"mas":"index"})

class RegisterView(APIView):
    """
    用户注册视图
    根据用户信息检测是否已注册，如若未注册则注册，否则显示提示信息。
    :mthod: POST
    :param: username     用户名
    :param: password     密码
    :param: re_password  重复密码
    :param: phone        手机号
    :param: email        邮箱地址
    """

    def post(self, request):
        form = forms.RegisterForm(request.data)
        response = MyResponse()
        if form.is_valid():
            clean_data = form.cleaned_data
            username = clean_data.get("username")
            password = clean_data.get("password")
            phone = clean_data.get("phone")
            email = clean_data.get("email")

            with transaction.atomic():
                user = User.objects.create(username=username,
                                           password=password,
                                           phone=phone,
                                           email=email)
            response.data = UserSerializer(user).data
            return Response(response.to_dict())

        else:
            msg = form.errors[list(form.errors.keys())[0]][0]
            return Response(response.error_response(msg=msg))

