from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

from django.db import DatabaseError

from redis.exceptions import RedisError


def exception_handler(exc, context):
    """
    自定义异常处理
    :param:  exc       异常
    :param:  context   抛出异常的上下文
    :return: Response 响应对象
    """
    # 先调用DRF原生的异常处理方法
    response = drf_exception_handler

    # 自定义异常处理
    if response is None:
        view = context["view"]

        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            response = Response({"msg": "服务区内部错误"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    return response


class MyException(Exception):
    """
    自定义异常类，用于抛出和捕获异常
    """
    def __init__(self, msg):
        self.msg = msg
        