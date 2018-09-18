# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/8/8 20:21'

import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from .models import VerifyCode

User = get_user_model()

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        """
        #手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")


        #验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        #验证发送频率
        time_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        if VerifyCode.objects.filter(add_time__gt=time_ago,mobile=mobile).count():
            raise serializers.ValidationError("发送频率过快")

        return mobile


class UserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6,help_text="验证码",error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"})
    username = serializers.CharField(label="用户名", max_length=50, allow_blank=False, validators=[UniqueValidator(
        queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, label="密码"
    )

    def create(self, validated_data):
        user = super(UserSerializer,self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        # 验证发送频率
        time_ago = datetime.now() - timedelta(hours=0, minutes=20, seconds=0)
        # if VerifyCode.objects.filter(add_time__gt=time_ago, mobile=mobile).count():
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            time_ago = datetime.now() - timedelta(hours=0, minutes=20, seconds=0)
            if time_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码获取失败")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """
    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")






