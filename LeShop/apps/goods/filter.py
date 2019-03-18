import django_filters
from .models import Goods
from django.db.models import Q


class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品过滤类
    '''

    # 两个参数，name是要过滤的字段，lookup是执行的行为，“小于等于本店价格”
    # 对shop_price 字段进行大于等于查询

    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text='最低价格')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte', help_text='最高价格')

    # 某个分类下的商品信息 （传进这个分类id）  自定义过滤器方法
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        # 去数据库里面 把查询出来的数据 进行过滤
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax','is_hot']
