from rest_framework import mixins
from rest_framework import viewsets
from .models import UserFav
from .serializers import UserFavSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsUserOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

# Create your views here.
class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    用户收藏
    '''
    serializer_class = UserFavSerializer
    # permission 是用来做权限判断的
    # IsAuthticated：必须登录用户     IsUserOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated,IsUserOrReadOnly)
    # auth是用来做用户认证的
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    # 搜索的字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只能查看当前用户的收藏，不会获取所有用户的收藏
        return UserFav.objects.filter(user=self.request.user)


