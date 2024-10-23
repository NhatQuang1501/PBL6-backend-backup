from rest_framework import serializers
from .utils import get_tokens_for_user
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from .models import *
from .enums import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_verified = False
        user.save()

        print(user)
        return user


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    role = serializers.CharField(write_only=True, required=False)

    default_error_messages = {
        "username": "Username phải chứa ít nhất một ký tự chữ cái"
    }

    class Meta:
        model = User
        fields = ["email", "username", "password", "role"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")
        if not any(char.isalpha() for char in username):
            raise serializers.ValidationError(self.default_error_messages["username"])
        return attrs

    def create(self, validated_data):
        role_name = validated_data.pop("role", "user")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        User.objects.assign_role(user, role_name)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(required=False)
    user_id = serializers.UUIDField(source="user.user_id", read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "user_id",
            "user",
            "fullname",
            "city",
            "birthdate",
            "phone_number",
            "gender",
            "avatar",
        ]
        extra_kwargs = {
            "user_id": {"read_only": True},
            "fullname": {"required": False},
            "city": {"required": False},
            "birthdate": {"required": False},
            "phone_number": {"required": False},
            "gender": {"required": False},
            "avatar": {"required": False},
        }

    def validate(self, data):
        if not self.instance and "user" not in data:
            raise serializers.ValidationError(
                {"user": "Hãy điền thông tin tài khoản đúng cú pháp"}
            )

        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        for field in rep:
            if rep[field] is None:
                rep[field] = "Chưa có thông tin"

            elif field == "gender":
                rep[field] = Gender.map_value_to_display(rep[field])

        return rep

    def to_internal_value(self, data):
        data = data.copy()
        gender = data.get("gender", None)

        if gender:
            data["gender"] = Gender.map_display_to_value(str(gender))

        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        user.is_verified = False
        user.save()

        user_profile = UserProfile.objects.create(user=user, **validated_data)

        return user_profile

    def update(self, instance, validated_data):
        instance.fullname = validated_data.get("fullname", instance.fullname)
        instance.city = validated_data.get("city", instance.city)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.gender = validated_data.get("gender", instance.gender)
        avatar = validated_data.get("avatar", None)

        if avatar:
            if isinstance(avatar, list):
                avatar = avatar[0]
            instance.avatar = avatar

        instance.save()

        return instance
