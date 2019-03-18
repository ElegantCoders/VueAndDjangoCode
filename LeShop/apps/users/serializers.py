from rest_framework import serializers
from LeShop import settings
import re
from datetime import datetime, timedelta
from .models import VerifyCode
# 和下面两句代码意思一样   都是获取UserProfile模型
# from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework.validators import UniqueValidator


# 发送验证码时候  他传手机号
class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, label="手机号", help_text="请输入手机号")

    def validate_mobile(self, mobile):

        # 1. 手机号是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经注册')

        # 2. 正则表达式 手机号是否合法
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号不正确')
        # 3. 判断验证码发送频率 60s之内只能发一次
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError('60s之内只能发送一次短信')

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册
    '''

    # UserProfile中没有code字段，这里需要自定义一个code序列化字段
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 }, label='验证码', write_only=True)

    username = serializers.CharField(
        label='用户名',
        validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')]
    )

    # 使用<input="password">作为输入
    password = serializers.CharField(
        label='密码',
        style={'input_type': 'password'},
        write_only=True
    )

    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validated_code(self, code):
        # 1.验证码正确性  2.时效
        # initial_data 用户从客户端post  传过来的数据
        # 拿到某个号码下的所有验证码  时间倒叙
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

        if verify_records:
            # 用户发送过验证码
            # 判断时间
            last_recode = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_recode.add_time:
                raise serializers.ValidationError('验证码过期')

            if code != last_recode.code:
                raise serializers.ValidationError('验证码错误')


        else:
            # 用户根本没有发送过验证码
            raise serializers.ValidationError('请输入正确验证码！')

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    # 验证用户名是否存在
    # username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
    #                                  validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    class Meta:
        model = User
        fields = ['username', 'mobile', 'code', 'password']
