from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """

    class Meta:
        model = User
        fields = ("username", "phone", "email")
