import datetime


from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

from django_redis import get_redis_connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from . import forms
from .models import User
from .serializers import UserSerializer
from utils.response import MyResponse
from utils.exception import MyException
from utils import constans
from libs.captcha.captcha import captcha


# Create your views here.

class BaseView():
    """
    基础视图类，用于继承，提供 校验用户 校验密码 校验验证码 签发jwt
    """

    def get_user(self, username):
        """
        获取用户对象
        :param: username   用户名(用户名、手机号、邮箱)
        :return: user_obj  用户对象
        """
        try:
            user_obj = User.objects.get(Q(username=username)|Q(phone=username)|Q(email=username))
        except User.DoesNotExist:
            raise MyException("用户不存在!")
        
        return user_obj

    def check_password(self, user, password):
        """
        密码校验
        :param: user     用户对象
        :param: password 用户输入密码
        :return: if user object password quual password return Ture else raise exception
        """
        if not user.password == password:
            self.is_freeze(user)
            raise MyException("密码错误,请重新输入!")
        
        redis_conn = get_redis_connection("error_password")
        if redis_conn.get("freeze_%s" % user.username):
            raise MyException("密码输入错误5次，请一天后再试!")

        return True

    def is_freeze(self, user):
        """
        用户冻结校验，一天内输错密码5次，就冻结帐号一天
        :param: user 用户对象
        """
        redis_conn = get_redis_connection("error_password")
        error_count = redis_conn.get("username_%s" % user.username)

        if not error_count:
            redis_conn.setex("username_%s" % user.username, constans.PASSWORD_ERROR_REDIS_EXPIRES, "1")

        elif int(error_count) == 5:
            redis_conn.setex("freeze_%s" % user.username, constans.FREEZE_USER_REDIS_EXPIRES, "1")

        else:
            error_count = int(error_count)
            error_count += 1
            redis_conn.setex("username_%s" % user.username, constans.PASSWORD_ERROR_REDIS_EXPIRES, str(error_count))

    def checke_captcha(self, image_code_id, image_code):
        """
        验证码校验 
        :param: image_code_id   redis中保存的验证码ID  
        :param: image_code      用户输入的验证码
        :return: if user input image_code equal redis save image_code return Ture else raise exception
        """
        redis_conn = get_redis_connection("verify_codes")
        redis_image_code = redis_conn.get("img_%s" % image_code_id)
        if not redis_image_code:
            raise MyException("验证码已过期，请重新获取!")
        if redis_image_code.decode("utf-8").lower() != image_code:
            raise MyException("验证码错误!")
        redis_conn.delete("img_%s" % image_code_id)
        return True

    def login_success(self, user):
        """
        登陆成功后签发jwt
        :param: user 用户对象
        :return: token、username、user_id
        """
        # 修改用户最近登陆时间
        user.last_login = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
        user.save()

        # 签发token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return {
            "token": token,
            "username": user.username,
            "user_id": user.id
        }



class RegisterView(APIView):
    """
    用户注册视图
    根据用户信息检测是否已注册，如若未注册则注册，否则显示提示信息。
    :method: POST
    :param: username     用户名
    :param: password     密码
    :param: re_password  重复密码
    :param: phone        手机号
    :param: email        邮箱地址
    :return: if seccess return user info else return error info
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

class CaptchaView(APIView):
    """
    获取验证码接口
    :method: GET
    :param: image_code_id 验证码ID
    :return: captcha image
    """
    def get(self, request):
        image_code_id = request.GET.get("image_code_id")

        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % image_code_id, constans.IMAGE_CODE_REDIS_EXPIRES, text)
        print(text)
        return HttpResponse(image, content_type="images/jpg")

class LoginView(BaseView, APIView):
    """
    登陆接口，使用 用户名|邮箱|手机号 + 密码 + 验证码 的搭配登陆 
    :method: POST
    :param: username      用户名 可以用 用户名|邮箱|手机号
    :param: password      密码
    :param: image_code_id 验证码ID
    :param: image_code    验证码
    """

    def post(self, request):
        response = MyResponse()
        form = forms.LoginForm(request.data)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            image_code_id = form.cleaned_data.get("image_code_id")
            image_code = form.cleaned_data.get("image_code")
            try:
                user_obj = self.get_user(username)
                self.checke_captcha(image_code_id, image_code)
                self.check_password(user_obj, password)
            except MyException as e:
                return Response(response.error_response(e.msg))
            response.data = self.login_success(user_obj)
            return Response(response.to_dict())
        else:
            msg = form.errors[list(form.errors.keys())[0]][0]
            return Response(response.error_response(msg=msg))

