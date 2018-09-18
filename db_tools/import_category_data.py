# -*- coding = utf-8 -*-
__author__ = 'cannon'
__date__ = '2018/7/28 20:13'

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
from apps.goods.models import GoodsCategory
from db_tools.data.category_data import row_data

# all_category = GoodsCategory.objects.all()


def get_level_data():
    for level_first in row_data:
        level_first_data = GoodsCategory()
        level_first_data.name = level_first['name']
        level_first_data.code = level_first['code']
        level_first_data.category_type = 1
        level_first_data.save()

        for level_second in level_first['sub_categorys']:
            level_second_data = GoodsCategory()
            level_second_data.name = level_second['name']
            level_second_data.code = level_second['code']
            level_second_data.category_type = 2
            level_second_data.parent_category = level_first_data
            level_second_data.save()

            for level_third in level_second['sub_categorys']:
                level_third_data = GoodsCategory()
                level_third_data.name = level_third['name']
                level_third_data.code = level_third['code']
                level_third_data.category_type = 3
                level_third_data.parent_category = level_second_data
                level_third_data.save()


if __name__ == '__main__':
    get_level_data()
    pass





