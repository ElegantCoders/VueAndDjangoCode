# DRG的序列化模块
from rest_framework import serializers
# 模型类
from .models import Goods, GoodsCategory, Banner,GoodsImage


class GoodsImagesSerialer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ['image']


class GoodsSerializer(serializers.ModelSerializer):
    '''
    商品序列化
    '''
    images = GoodsImagesSerialer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class CategorySerializer3(serializers.ModelSerializer):  # 3
    '''
    三级类目
    '''

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):  # 2
    '''
    二级类目
    '''
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):  # 1
    '''
    一级类目
    '''
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
