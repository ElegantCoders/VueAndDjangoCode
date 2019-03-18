from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend  # 导入我们的自定义过滤模块
from rest_framework import filters  # 过滤器

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer, BannerSerializer
from .filter import GoodsFilter


class GoodsPagination(PageNumberPagination):
    """     商品列表自定义分页     """
    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = "page"
    # 做多能显示多少页
    max_page_size = 100


class GoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    商品列表页
    '''
    pagination_class = GoodsPagination
    serializer_class = GoodsSerializer
    queryset = Goods.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 过滤组件  搜索组件  排序组件
    # 设置filter的类为我们自定义的
    filter_class = GoodsFilter
    # 搜索,=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('name', 'goods_brief')

    # 排序
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)  # 取出所有一级类目
    serializer_class = CategorySerializer  # 序列化使用的序列化类


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    首页轮播图
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer
