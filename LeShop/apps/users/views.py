from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import SmsSerializer, UserRegSerializer
from random import choice
from utils.huaxin import HuaXin
from LeShop import settings
from .models import VerifyCode, UserProfile

from rest_framework_jwt.settings import api_settings


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SmsSerializer

    def generate_code(self):
        '''
        生成四位数的数字验证码
        '''
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        # 父类做的事情 就是存一个模型类到数据库  添加一条新的数据
        # 在父类的基础上
        # 1. 发送短信验证码  (随机生成一个字符) 4位
        # 2. 发送   HuaXin
        # 3. 接受返回值   returnstatus = Success  表示成功
        # 4. 保存这个验证码

        # 获取序列化的类
        serializer = self.get_serializer(data=request.data)
        # 验证手机号的合法性
        serializer.is_valid(raise_exception=True)

        # 可用的手机号
        huaxin = HuaXin(settings.ACCOUNT, settings.PASSWORD)

        # 生成验证码
        code = self.generate_code()

        # 得到手机号     validated_data-->可以拿到序列化里面的字段
        sms_status = huaxin.send_sms(code, mobile=serializer.validated_data['mobile'])

        if sms_status['returnstatus'] != 'Success':
            # 失败
            return Response(sms_status['message'], status=status.HTTP_400_BAD_REQUEST)

        else:
            # 成功
            VerifyCode(code=code, mobile=serializer.validated_data['mobile']).save()
            return Response(sms_status['message'], status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # 获取序列化数据
        serializer.is_valid(raise_exception=True)  # 验证
        # User就是最终 注册的用户
        user = self.perform_create(serializer)

        # 帮他登录

        # 登录成功之后要给用户返回的数据
        ret_dict = serializer.data

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        ret_dict['token'] = token
        ret_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 保存
        return serializer.save()
