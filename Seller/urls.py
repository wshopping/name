from django.urls import path,re_path
from django.contrib import admin
from Seller.views import index,goods_add,goods_list,login,example,logout,goods_change,goods_del
urlpatterns = [
    re_path('^$', index),
    path('index/', index),
    path('login/', login),
    path('logout/', logout),
    path('goods_add/', goods_add, name = "goods_add"),
    path('goods_list/', goods_list, name = "goods_list"),
    re_path('goods_change/(?P<id>\d+)/', goods_change, name="goods_change"),
    re_path('goods_del/(?P<id>\d+)/', goods_del, name="goods_del"),
    path('example/', example),


]