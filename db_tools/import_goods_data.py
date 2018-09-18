# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/29 22:07'


import os
import sys
#  获取当前文件的路径，以及路径的父级文件夹名
pwd = os.path.dirname(os.path.realpath(__file__))
# 将项目目录加入setting
sys.path.append(pwd + "../")
# 获取manage.py中的设置值
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "martonline.settings")

#设置django，保证可以使用model
import django
django.setup()

#有顺序关系，上面条件导入了设置，所以不能超前导入model
from apps.goods.models import Goods,GoodsImage,GoodsCategory
from db_tools.data.product_data import row_data


def get_goods_data():

    row_length = len(row_data)
    cnt = 0
    for goods_data in row_data:
        goods = Goods()
        goods.name = goods_data["name"]
        goods.goods_desc = goods_data["desc"] if goods_data["desc"] is not None else ""
        goods.market_price = float(int(goods_data["market_price"].replace("￥", "").replace("元", "")))
        goods.shop_price = float(int(goods_data["sale_price"].replace("￥", "").replace("元", "")))
        goods.goods_brief = goods_data["goods_desc"] if goods_data["goods_desc"] is not None else ""
        goods.goods_front_image = goods_data["images"][0] if goods_data["images"] is not None else ""

        category_name = goods_data["categorys"][-1]
        # 取出当前子类对应的GoodsCategory对象，filter没有匹配的会返回空数组，不会抛异常。

        category = GoodsCategory.objects.filter(name=category_name)
        if category:
            goods.category = category[0]

        cnt = cnt + 1
        print("@@@@  " + str(cnt))
        print(goods.name)
        print(goods.category)
        print(goods.goods_desc)
        goods.save()


        for goods_image in goods_data["images"]:
            goods_image_instance = GoodsImage()
            goods_image_instance.goods = goods
            goods_image_instance.image = goods_image
            goods_image_instance.save()

    print("###   " + str(row_length))



if __name__ == '__main__':
    get_goods_data()
    pass


