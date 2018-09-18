from datetime import datetime


from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer



from rest_framework.views import APIView
from utils.alipay import AliPay
from martonline.settings import ali_pub_key_path, private_key_path
from rest_framework.response import Response


# Create your views here.


class ShoppingCartViewSet(ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShoppingCartSerializer


    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.store_num -= instance.nums
        goods.save()



    def perform_destroy(self, instance):
        goods = instance.goods
        goods.store_num += instance.nums
        goods.save()
        instance.delete()


    def perform_update(self, serializer):
        cart_id = serializer.instance.id
        existed_cart = ShoppingCart.objects.filter(id=cart_id)
        if existed_cart:
            old_nums = existed_cart[0].nums
        else:
            pass
        new_cart = serializer.save()
        new_nums = new_cart.nums
        goods = new_cart.goods
        goods.store_num -= (new_nums-old_nums)
        goods.save()



class OrderViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    订单功能
    list:
        获取订单列表
    create：
        生成订单
    delete：
        取消订单
    retireve：
        订单详情
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer


    def perform_create(self, serializer):
        order = serializer.save()
        # 获取到用户购物车里的商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


class AliPayView(APIView):
    def get(self, request):
        """

        :param request:
        :return:
        处理支付宝return_url返回
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            # appid在沙箱环境中就可以找到
            appid="2016091700534111",
            app_notify_url="http://47.104.226.243:8000/alipay/return/",
            # 个人私有的密钥
            app_private_key_path=private_key_path,
            # 支付宝的公钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,

            return_url="http://47.104.226.243:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response


    def post(self, request):
        """

        :param request:
        :return:
        处理支付宝return_url返回
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            # appid在沙箱环境中就可以找到
            appid="2016091700534111",
            app_notify_url="http://47.104.226.243:8000/alipay/return/",
            # 个人私有的密钥
            app_private_key_path=private_key_path,
            # 支付宝的公钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用
        # debug为true时使用沙箱的url。如果不是用正式环境的url
        debug = True,  # 默认False,

                return_url = "http://47.104.226.243:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        # 如果验签成功
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            # 将success返回给支付宝，支付宝就不会一直不停的继续发消息了。
            return Response("success")



