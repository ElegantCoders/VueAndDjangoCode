from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    '''
    用户
    '''
    GENDER_CHOICES = (
        ("male", u"男"),  # 加u是为了兼容python2
        ("female", u"女")
    )

    name = models.CharField(max_length=32, null=True, blank=True, verbose_name="姓名")  # blank=True 表示前端输入框可以为空
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电 话")
    email = models.EmailField(max_length=128, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class VerifyCode(models.Model):
    '''
    短信验证码
    '''

    code = models.CharField(max_length=32, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code