from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from utils.base_model import BaseModel

# Create your models here.
class User(BaseModel, AbstractBaseUser):
    """
    用户模型
    """
    username = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    phone = models.CharField(max_length=11, verbose_name="手机号")
    email = models.CharField(max_length=128, verbose_name="邮箱")
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        db_table = "aley_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name