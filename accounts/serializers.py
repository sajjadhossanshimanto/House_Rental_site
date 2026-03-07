from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'address', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'address', 'profile_image', 'role', 'is_email_verified', 'created_at')
        read_only_fields = ('id', 'role', 'is_email_verified', 'created_at')
