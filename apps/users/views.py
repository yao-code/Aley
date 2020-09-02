from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse

# Create your views here.

def index(request):
    return JsonResponse({"mas":"index"})

class RegisterView(APIView):

    def post(self, request):
        return JsonResponse({"msg":"hello"})

