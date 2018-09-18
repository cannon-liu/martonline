from django.db import models
from django.contrib.auth.models import AbstractUser


#system自带
from datetime import datetime
# Create your models here.


#用户信息
class UserProfile(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="用户名称")
    birthday = models.DateField(null=True, blank=True,verbose_name="用户生日")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="用户手机")
    gender = models.CharField(max_length=10, choices=(('male', u'男'), ('female', u'女')), default='male',
                              verbose_name="性别")
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name="用户邮箱")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = 'user_info'

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    code = models.CharField(max_length=200, null=True, blank=True, verbose_name="验证码")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="用户手机")
    add_time = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = verbose_name
        db_table = 'verifycode'

    def __str__(self):
        return self.code
