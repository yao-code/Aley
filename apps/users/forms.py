import re

from django import forms
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(forms.Form):
    """
    注册表单的限制
    """
    username = forms.CharField(error_messages={"required":"该字段不能为空"})
    password = forms.CharField(error_messages={"required":"该字段不能为空"})
    re_password = forms.CharField(error_messages={"required":"该字段不能为空"})
    phone = forms.CharField(error_messages={"required":"该字段不能为空"})
    email = forms.CharField(error_messages={"required":"该字段不能为空"})

    def clean_username(self):
        """
        局部钩子
        验证用户名的唯一性
        """
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            raise ValidationError("用户名长度必须大于等于4!")

        if User.objects.filter(username=username):
            raise ValidationError("用户名重复!")

        else:
            return username

    def clean_phone(self):
        """
        局部钩子
        验证手机号码的有效性
        """
        phone = self.cleaned_data.get("phone")

        if len(phone) != 11 and not re.match(r"/^[1](([3][0-9])|([4][5-9])|([5][0-3,5-9])|([6][5,6])|([7][0-8])|([8][0-9])|([9][1,8,9]))[0-9]{8}$/", phone):
            raise ValidationError("请输入正确的手机号码!")

        if User.objects.filter(phone=phone):
            raise ValidationError("该手机号已被注册!")
        return phone

    def clean_email(self):
        """
        局部钩子
        验证邮箱地址的有效性
        """
        email = self.cleaned_data.get("email")

        if not re.match(r"", email):
            raise ValidationError("请输入正确的邮箱地址!")

        if User.objects.filter(email=email):
            raise ValidationError("该邮箱已被注册!")
        return email

    def clean(self):
        """
        全局钩子
        检测密码是否一致,以及密码复杂度
        """
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if password != re_password:
            raise ValidationError("两次密码输入不一致!")

        if not re.match(r"^(?=.*[0-9].*)(?=.*[A=Z].*)(?=.*[a-z].*).{8,30}", password):
            raise ValidationError("密码长度至少为8,且必须包含至少一个数字，一个大写字母，一个小写字母!")
        return self.cleaned_data
