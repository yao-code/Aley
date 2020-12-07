from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

# from tenacity import retry
# from tenacity import wait_fixed
# from tenacity import stop_after_attempt
# from tenacity import stop_after_delay
# from tenacity import retry_if_exception_type
# from tenacity import retry_if_result
# from tenacity import retry_error_callback
from tenacity import *

from utils.response import MyResponse


# Create your views here.

def is_false(value):
    print(type(value))
    print(value.data)  # 获取 Response 的数据 
    return False

def return_last_value(retry_state):
    print("执行回调函数")
    return retry_state.outcome.result()


class Test_1(APIView):

    @retry  # 不间断重试 无限重试
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_2(APIView):

    @retry(wait=wait_fixed(2))  # 隔2s重试一次 无限重试
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_3(APIView):

    @retry(stop=stop_after_attempt(5))  # 限制重试次数
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_4(APIView):

    @retry(stop=stop_after_delay(5))  # 限制重试时间
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_5(APIView):

    @retry(stop=(stop_after_attempt(5) | stop_after_delay(5)))  # 重试限制满足其一就停止
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_6(APIView):

    @retry(retry=retry_if_exception_type(KeyError), stop=stop_after_attempt(5))  # 指定错误重试
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_7(APIView):

    @retry(retry=retry_if_result(is_false))  # 满足条件时重试 返回 True 就重试 False 就不重试 
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_8(APIView):

    @retry(stop=stop_after_attempt(5), reraise=True)  # retry 之后抛出的时 retry.Error 添加 reraise=True 原样抛出错误 
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())


class Test_9(APIView):

    @retry(stop=stop_after_attempt(5), retry_error_callback=return_last_value)  # 重试失败后执行回调函数
    def get(self, request):
        response = MyResponse()
        print("正在重试。。。")
        raise KeyError
        return Response(response.to_dict())