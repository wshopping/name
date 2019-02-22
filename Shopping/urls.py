"""Shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include,re_path
from Buyyer.views import index,login,register,logout,register_email,callbackPay,paymethod
from Seller.views import goods_change,GoodsApi,example
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cc/', include('Seller.urls')),
    path('buyyer/', include("Buyyer.urls")),
    path('ckeditor/', include("ckeditor_uploader.urls")),
]
urlpatterns += [
    re_path('^$', index),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('register_email/', register_email),

    re_path('goods_change/(?P<id>\d+)/', goods_change, name="goods_change"),

]
import  Buyyer
handler404 = Buyyer.views.page_not_found



urlpatterns += [
    path('Api/goods/', GoodsApi.as_view()),
    path('Api/example/', example),
    path('callbackPay/', callbackPay),
    re_path('paymethod/(\d+)/', paymethod),
]