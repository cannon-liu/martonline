import random

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, permissions, authentication
from rest_framework.permissions import IsAuthenticated


from .serializers import SmsSerializer, UserSerializer, UserDetailSerializer
from utils.yunpian import YunPian
from martonline.settings import Yunpian_Apikey, SMS_sendtime
from .models import VerifyCode
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.
User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(
                Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    """
    发送短信
    """
    serializer_class = SmsSerializer

    def generate_code(self):

        code = ""
        for i in range(0, 6):
            num = random.randint(0, 9)
            code = code + str(num)

        return code

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  #抛出异常后，就直接终止，给出400的错误
        mobile = serializer.validated_data["mobile"]
        code = self.generate_code()
        yun_pian = YunPian(Yunpian_Apikey)
        sms_send = yun_pian.send_sms(code, SMS_sendtime, mobile)
        if sms_send._code!= 0:
            return Response({
                "mobile": sms_send._msg
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    用户
    """
    # serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserSerializer

        return UserDetailSerializer


    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        re_dict["token"] = token
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写该方法，不管传什么id，都只返回当前用户,用于用户中心
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()





