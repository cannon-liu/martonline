# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/30 12:17'

from django.db.models import Q

from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage, Banner, Ad_Goods, GoodsCategoryBrand

#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoodsCategory
#         fields = "__all__"

class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)

class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"

class GoodsCategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"

class IndexCategorySerializer(serializers.ModelSerializer):
    brands = GoodsCategoryBrandSerializer(many=True)
    sub_cat = CategorySerializer2(many=True)
    goods = serializers.SerializerMethodField()
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    def get_ad_goods(self, obj):
        ad_goods = Ad_Goods.objects.filter(category_id=obj.id)
        if ad_goods:
            need_goods = ad_goods[0].goods
            ad_goods_serialzer = GoodsSerializer(need_goods, many=False, context={'request': self.context['request']})
            return ad_goods_serialzer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"