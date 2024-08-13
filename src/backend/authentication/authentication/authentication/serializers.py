from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.base import ModelBase
from django.contrib.auth import authenticate
from rest_framework import serializers
from typing import Dict, List
from .models import User
import logging

logger = logging.getLogger(__name__)


class UserSerializerRegister(serializers.ModelSerializer):
    password: serializers.CharField = serializers.CharField(
        write_only=True, required=True
    )

    class Meta:
        model: ModelBase = User
        fields: List = ["username", "email", "password"]

    def create(self, validated_data) -> User:
        print(f"validated_data ->: {validated_data}")
        user: User = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            ip=self.context["request"].META.get("REMOTE_ADDR"),
            ip_last_login=self.context["request"].META.get("REMOTE_ADDR"),
        )
        logger.info(f"User {user.username} created")
        return user


class UserSerializerLogin(serializers.Serializer):
    username: serializers.CharField = serializers.CharField(required=True)
    password: serializers.CharField = serializers.CharField(required=True)

    def validate(self, attrs) -> User:
        print(f"attrs ->: {attrs}")

        user = authenticate(
            username=attrs.get("username"), password=attrs.get("password")
        )
        if user is not None and user.is_active:
            user.ip_last_login = self.context["request"].META.get("REMOTE_ADDR")
            user.save()
            return user
        print("sale un error")
        raise serializers.ValidationError("Incorrect Credentials")
