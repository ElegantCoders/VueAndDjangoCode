"""LeShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.static import serve
from LeShop.settings import MEDIA_ROOT
from django.conf.urls import url, include
#from rest_framework.authtoken import views  # DRF内置的认证组件
from rest_framework_jwt.views import obtain_jwt_token
import xadmin

from rest_framework.routers import DefaultRouter
from goods.views import GoodsViewSet, CategoryViewset, BannerViewset
from users.views import SmsCodeViewset,UserViewset
from user_operation.views import UserFavViewset


router = DefaultRouter()
router.register(r'goods', GoodsViewSet, base_name="goods")  # 商品的URL
router.register(r'categorys', CategoryViewset, base_name="categorys")  # 首页分类的URL
router.register(r'banners', BannerViewset, base_name="banners")  # 轮播图URL
router.register(r'code', SmsCodeViewset, base_name="code") # 验证码
router.register(r'users', UserViewset, base_name="users") # 注册
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

urlpatterns = [
    # url(r'login/',obtain_jwt_token), # 登录
    url(r'login/', obtain_jwt_token),
    url('xadmin/', xadmin.site.urls),
    url('ueditor/', include('DjangoUeditor.urls')),
    url(r'^', include(router.urls)),  # 商品列表页
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # 登录

    # 文件
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

]
