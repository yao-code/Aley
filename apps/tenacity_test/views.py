from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import GenericAPIView

# from tenacity import retry
# from tenacity import wait_fixed
# from tenacity import stop_after_attempt
# from tenacity import stop_after_delay
# from tenacity import retry_if_exception_type
# from tenacity import retry_if_result
# from tenacity import retry_error_callback
from tenacity import *

from utils.response import MyResponse

from users.models import User
from users.serializers import UserSerializer


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


class Data(APIView):
    """通过 request.data  获取参数 """

    def get(self, request):
        data = request.data  # 不能获取到get方法的参数
        print(data)
        return Response(MyResponse().to_dict())

    def post(self, request):
        data = request.data  # 可以获取到参数
        print(data)
        return Response(MyResponse().to_dict())

    def put(self, request):
        data = request.data  # 可以获取到参数
        print(data)
        return Response(MyResponse().to_dict())

    def delete(self, request):
        data = request.data  # 可以获取到参数
        print(data)
        return Response(MyResponse().to_dict())


class Query_Params(APIView):
    """
    通过 request.query_params 获取参数
    可以获取 GET 请求的所有参数
    可以获取任何请求以get方式传递的参数 e.g: post 请求可以获取到 params 里的参数 但是获取不到 body 里的参数
    """

    def get(self, request):
        data = request.query_params
        print(data)
        return Response(MyResponse().to_dict())

    def post(self, request):
        data = request.query_params 
        print(data)
        return Response(MyResponse().to_dict())

    def put(self, request):
        data = request.query_params
        print(data)
        return Response(MyResponse().to_dict())

    def delete(self, request):
        data = request.query_params
        print(data)
        return Response(MyResponse().to_dict())



class Parsers(APIView):
    # 设置局部的解析器
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        print(request.content_type)  # 返回表示 HTTP 请求正文的媒体类型（media type）的字符串对象
        print(request.stream)
        return Response({"data": request.data})


class TestResponse(APIView):

    def get(self, request):
        print(self.get_renderers())

        # print(self.get_parsers())

        # print(self.get_authenticators())

        # print(self.get_throttles())

        # print(self.get_permissions())

        # print(self.get_content_negotiator())

        # print(self.get_exception_handler())

        return Response({"data": "OK"})


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList2(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"
    lookup_url_kwarg = "uid"

    def get(self, request, uid=None):
        print(uid)
        response = MyResponse()
        if not uid:
            user_queryset = self.get_queryset()
            if user_queryset.exists():
                response.data = self.get_serializer(user_queryset, many=True).data
                return Response(response.to_dict())
            return Response(response.error_response("nothing"))

        else:
            user_obj = self.get_object()
            if user_obj:
                response.data = self.get_serializer(user_obj).data
                return Response(response.to_dict())
            return Response(response.error_response("no one"))





