"""martonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from extra_apps import xadmin
from martonline.settings import MEDIA_ROOT
# from martonline.settings import STATIC_ROOT
from django.views.static import serve
from django.views.generic import TemplateView

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token


from apps.goods.views import GoodsListViewSet, CategoryViewSet, BannersViewSet, IndexCategoryViewSet
from apps.user.views import SmsCodeViewSet, UserViewSet
from apps.operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from apps.trade.views import ShoppingCartViewSet, OrderViewSet, AliPayView
# goodslist = GoodsListViewSet.as_view({
#     'get': 'list'
# })

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods")
router.register(r'categorys', CategoryViewSet, base_name="categorys")
router.register(r'smscode', SmsCodeViewSet, base_name="smscode")
router.register(r'users', UserViewSet, base_name="user")
router.register(r'userfavs', UserFavViewSet, base_name="userfav")
router.register(r'users', UserViewSet, base_name="user")
router.register(r'messages', UserLeavingMessageViewSet, base_name="usermessage")
router.register(r'address', UserAddressViewSet, base_name="useraddress")
router.register(r'shopcarts', ShoppingCartViewSet, base_name="shopcarts")
router.register(r'orders', OrderViewSet, base_name="orders")
router.register(r'banners', BannersViewSet, base_name="banners")
router.register(r'indexgoods', IndexCategoryViewSet, base_name="indexgoods")


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # path('static/<path:path>', serve, {'document_root': STATIC_ROOT}),
    #


    path(r'index/', TemplateView.as_view(template_name="index.html"), name="index"),

    path("alipay/return/", AliPayView.as_view(), name="alipay"),

    path(r'docs/', include_docs_urls(title="cannon martonline")),

    #drf自带的token认证模式
    # path(r'^api-token-auth/', views.obtain_auth_token)
    # path(r'^api-auth/', include('rest_framework.urls')),

    #jwt认证模式

    path(r'login/', obtain_jwt_token),
    # path('goods/', goodslist, name='goods'),
    re_path(r'^', include(router.urls)),


]
