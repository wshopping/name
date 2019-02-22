
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,render_to_response
from Buyyer.models import Buyer
from Seller.views import setPassword
from Seller.models import Goods





def cookieValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        username = cookie.get("user_name")
        session = request.session.get("username") #获取session
        user = Buyer.objects.filter(username = username).first()
        if user and session == username: #校验session
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login/")
    return inner

@cookieValid
def index(request):
    data = []
    goods = Goods.objects.all()
    for good in goods:
        good_img = good.image_set.first()
        img = good_img.img_adress.url
        data.append(
            {"id":good.id,"img": img.replace("media","static"), "name": good.goods_name, "price": good.goods_now_price}
        )
    return render(request,"buyyer/index.html",{"datas": data})

def login(request):
    result = {"statue": "error","data": ""}
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        user = Buyer.objects.filter(username = username).first()
        if user:
            password = setPassword(request.POST.get("userpass"))
            db_password = user.password
            if password == db_password:
                response = HttpResponseRedirect("/")
                response.set_cookie('user_id',user.id)
                response.set_cookie('user_name', user.username)
                request.session["username"] = user.username
                return response
            else:
                result["data"] = "密码错误"
        else:
            result["data"] = "用户名不存在"
    return render(request,'buyyer/login.html',{"result":result})

def register(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("userpass")
        buyer = Buyer()
        buyer.username = username
        buyer.password = setPassword(password)
        buyer.save()
        return HttpResponseRedirect("/login/")
    return render(request,'buyyer/register.html')

def logout(request):
    response = HttpResponseRedirect("/login/")
    response.delete_cookie("user_name")
    response.delete_cookie("user_id")
    del request.session["username"]
    return response


import time
import datetime
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from Buyyer.models import EmailValid

import random

def getRandomData():
    result = str(random.randint(1000,9999))
    return result

def sendMessage(request):
    result = {"staue": "error","data":""}
    if request.method == "GET" and request.GET:
        recver = request.GET.get("email")
        try:
            subject = "邮件"
            text_content = "hello python"
            value = getRandomData()
            html_content = """
            <div>
                <p>
                    尊敬的q商城用户，您的用户验证码是:%s,不要告诉别人。
                </p>
            </div>
            """%value
            message = EmailMultiAlternatives(subject,text_content,"17864112455@163.com",[recver])
            message.attach_alternative(html_content,"text/html")
            message.send()
        except Exception as e:
            result["data"] = str(e)
        else:
            result["staue"] = "success"
            result["data"] = "success"
            email = EmailValid()
            email.value = value
            email.times = datetime.datetime.now()
            email.email_address = recver
            email.save()
        finally:
            return JsonResponse(result)

def register_email(request):
    result = {"statu": "error","data":""}
    if request.method == "POST" and request.POST:

        username = request.POST.get("username")
        code = request.POST.get("code")
        userpass = request.POST.get("userpass")
        email = EmailValid.objects.filter(email_address = username).first()
        if email:
            if code == email.value:
                now = time.mktime(
                    datetime.datetime.now().timetuple()
                )
                db_now = time.mktime(email.times.timetuple())
                if now - db_now >= 86400:
                    result["data"] = "验证码过期"
                    email.delelt()
                else:
                    buyer = Buyer()
                    buyer.username = username
                    buyer.email = username
                    buyer.password = setPassword(userpass)
                    buyer.save()
                    result["statu"] = "success"
                    result["data"] = "恭喜！注册成功"
                    email.delete()
                    return HttpResponseRedirect("/login/")
            else:
                result["data"] = "验证码错误"
        else:
            result["data"] = "验证码不存在"
    return render(request, 'buyyer/register_mail.html',locals())

def goods_details(request,id):
    good = Goods.objects.get(id=int(id)) #一个商品
    good_img = good.image_set.first().img_adress.url.replace("media","static")

    seller = good.seller #商品对应的商铺 外键 --> 主
    goods = seller.goods_set.all() #主 --> 外
    data = []
    for g in goods:
        goods_img = g.image_set.first()
        img = goods_img.img_adress.url
        data.append(
            {"id": g.id, "img": img.replace("media","static"), "name": g.goods_name, "price": g.goods_now_price}
        )
    return render(request,"buyyer/goods_details.html",locals())

from Buyyer.models import BuyCar
def carJump(request,goods_id):
    goods = Goods.objects.get(id = int(goods_id))
    id = request.COOKIES.get("user_id")  # 获取用户身份
    if request.method == "POST" and request.POST:
        count = request.POST.get("count")
        img = request.POST.get("good_img")
        buyCar = BuyCar.objects.filter(user = int(id),goods_id = int(goods_id)).first() #查询是否存在在购物车当中
        if not buyCar: #不存在
            buyCar = BuyCar() #实例化模型
            buyCar.goods_num = int(count) #添加数量
            buyCar.goods_id = goods.id
            buyCar.goods_name = goods.goods_name
            buyCar.goods_price = goods.goods_now_price
            buyCar.user = Buyer.objects.get(id=request.COOKIES.get("user_id"))
            buyCar.save()
        else: #存在
            buyCar.goods_num += int(count) #数量相加
            buyCar.save()
        all_price = float(buyCar.goods_price) * int(count)
        return render(request,"buyyer/buyCar_jump.html",locals())
    else:
        return HttpResponse("404 not fond")
@cookieValid
def carList(request):
    id=request.COOKIES.get("user_id") #获取用户身份
    goodList = BuyCar.objects.filter(user = int(id)) #查询指定用户的购物车商品信息
    address_list=Address.objects.filter(buyer=int(id))
    price_list = []
    for goods in goodList:
        g=Goods.objects.get(id=goods.goods_id)
        img =g.image_set.all().first().img_adress.url.replace("media","static")
        all_price = float(goods.goods_price) * int(goods.goods_num)
        price_list.append({"price": all_price, "goods": goods,"img":img}) #添加总数
    return render(request,"buyyer/car_list.html",locals())

@cookieValid
def delete_goods(request,goods_id):
    """
    删除一条
    """
    id = request.COOKIES.get("user_id")
    goods = BuyCar.objects.filter(user = int(id),goods_id = int(goods_id))
        #对应用户id
        #对应商品id
    goods.delete()
    return HttpResponseRedirect("http://172.21.0.6:8000/buyyer/carList/")
#127.0.0.1
@cookieValid
def clear_goods(request):
    """
    删除一条
    """
    id = request.COOKIES.get("user_id")
    goods = BuyCar.objects.filter(user = int(id))
    goods.delete()
    return HttpResponseRedirect("http://172.21.0.6:8000/buyyer/carList/")
from Buyyer.models import Order
from Buyyer.models import OrderGoods
def add_order(request):
    buyer_id =request.COOKIES.get("user_id")#用户的ID
    goods_list=[]#订单商品的列表
    if request.method=="POST"and request.POST:
        requestData=request.POST#请求数据
        addr=requestData.get("address")#寄送地址的id
        pay_method=requestData.get("pay_Method")#支付方式
        #获取商品信息
        all_price=0#总价
        for key,value in requestData.items():#循环所有的数据
            if key.startswith("name"):#如果键以name开头，我们就认为是商品信息的ID
                buyCar=BuyCar.objects.get(id=int(value))#获取商品

                g = Goods.objects.get(id=buyCar.goods_id)
                img = g.image_set.all().first().img_adress.url.replace("media", "static")

                price=float(buyCar.goods_num)*float(buyCar.goods_price)#单条商品的总价
                all_price+=price#加后总价
                goods_list.append({"price":price,"buyCar":buyCar,"img":img})#构建数据模型{”小计总价“：price，‘商品信息’：buyCar}
                #存入订单库
        Addr = Address.objects.get(id=int(addr))#获取地址数据
        order=Order()#保存到订单
        #订单编号 日期 +随机+订单 +id
        now=datetime.datetime.now()
        order.order_num=now.strftime("%Y-%m-%d")+str(random.randint(10000,99999))+str(order.id)
        order.order_time=now
        #状态 未支付1 支付成功2 配送中3 交易完成4 已取消0
        order.order_statue=1
        order.total=all_price
        order.user=Buyer.objects.get(id=int(buyer_id))
        order.order_address=Addr
        order.save()
        for good in goods_list:#循环保存订单当中的商品
            g=good["buyCar"]
            g_o=OrderGoods()
            g_o.goods_id=g.id
            g_o.goods_name=g.goods_name
            g_o.goods_pric=g.goods_price
            g_o.goods_num=g.goods_num
            g_o.goods_picture=g.goods_picture
            g_o.order =order
            g_o.save()
        return render(request,"buyyer/enterOrder.html",locals())
    else:
        return HttpResponseRedirect("/buyyer/carList/")
from Buyyer.models import Address
def addAddress(request):
    if request.method =="POST" and request.POST:
        buyer_id= request.COOKIES.get("user_id")
        buyer_name=request.POST.get("buyer")
        buyer_phone=request.POST.get("buyer_phone")
        buyer_address=request.POST.get("buyer_address")
        db_buyer=Buyer.objects.get(id=int(buyer_id))
        addr =Address()
        addr.recver=buyer_name
        addr.phone=buyer_phone
        addr.address=buyer_address
        addr.buyer=db_buyer
        addr.save()
        return HttpResponseRedirect("/buyyer/address/")
    return render(request,"buyyer/addAddress.html")
def address(request):
    buyer_id =request.COOKIES.get("user_id")
    address_list =Address.objects.filter(buyer=int(buyer_id))
    return render(request,"buyyer/address.html",locals())
def changeAddress(request,address_id):
    addr =Address.objects.get(id=int(address_id))
    if request.method=="POST" and request.POST:
        buyer_name=request.POST.get("buyer")
        buyer_phone=request.POST.get("buyer_phone")
        buyer_address=request.POST.get("buyer_address")
        addr.recver=buyer_name
        addr.phone=buyer_phone
        addr.address=buyer_address
        addr.save()
        return HttpResponseRedirect("/buyyer/address/")
    return render(request,"buyyer/addAddress.html",locals())
def delAddress(request,address_id):
    addr= Address.objects.get(id=int(address_id))
    addr.delete()
    return HttpResponseRedirect("/buyyer/address/")

from alipay import AliPay

def Pay(order_id,money):
  alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
  MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu6SgXfld6oy5+ElN87fesW5tXZ6jwJRJRuvHcblipnnPGZtLlZ+sOjHSOTqXhTuQucaX1QbsXAuK/KebjNodIWH/tUcBNnY1BMP5OuRvcbgpWgVCJoHa44E8gPiVpaxLAx1amvc+abc1QBg5Z6p9umT2Ze+54xazADGG+ceAvSM7XGlbwnIENjrjfDUJJtTAZ1EJyAvT2ZzN6KUgeXnxKJCZZuKuEzAS33CmQEchWEfcF27BszHKCi6tC7l+eAUoghFQE/TUV9unHuLQwTB382tJpgR8sRn6mTTER+5dX1dtoJQ/98KJ2STHdnlsx8uc14CyGtA7dDvxoya8m0DfpwIDAQAB
  -----END PUBLIC KEY-----'''

  app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
  MIIEpAIBAAKCAQEAu6SgXfld6oy5+ElN87fesW5tXZ6jwJRJRuvHcblipnnPGZtLlZ+sOjHSOTqXhTuQucaX1QbsXAuK/KebjNodIWH/tUcBNnY1BMP5OuRvcbgpWgVCJoHa44E8gPiVpaxLAx1amvc+abc1QBg5Z6p9umT2Ze+54xazADGG+ceAvSM7XGlbwnIENjrjfDUJJtTAZ1EJyAvT2ZzN6KUgeXnxKJCZZuKuEzAS33CmQEchWEfcF27BszHKCi6tC7l+eAUoghFQE/TUV9unHuLQwTB382tJpgR8sRn6mTTER+5dX1dtoJQ/98KJ2STHdnlsx8uc14CyGtA7dDvxoya8m0DfpwIDAQABAoIBAQCbO2kz9R098efTwIkNi9pePPWbEqdzpPkuA9Z+fZhgErtC+tc/09V+W0MH9zHslcd3+RQYtt6Ik0ALHnmvv62DtXf+ttwI+yeHZrzjfKG5mVoUT+9Wveygc4TjSUM7yNpRnFIdi1cFy/vwp1muKjxTHD0/PWAxvtCc41w/fU1Cqdw46KXwl3gaOzmpBqrLT7FR8eMzrb4Jm073W1+2YZ1bEanb1Rqd+MFR153uO5tko1QB4cHBXfv7G7NsZi9EscBEppppggrDP+Gm1wPd9ke7hvo2gCWK7fWZR8mAT2vIAkHKH1YYtKrAykQMVRuB1weTgRunQOXuwAUQVyA19/vpAoGBAOyjTyV5lkrjj8xaGu8/PkEa1dy4I50sA4hEitWn8wP/HKE+a50Q7SACJwWR+cKBbed3rV6DxZeP2KSwDB5kDLs+goGfvA4dRXsqTIVUepK9wM3e6Iiy/J0jOPb/zfSzb2iIMhQnjmAKUJAOz2bfrvKCpXbxa0DD/KmybXdVxI8lAoGBAMr/DlP89DeYA+5P9oJlveIc5OtWUrNANnAjdOI8un57AdvZRsswDmFAcyDamqE4rtfBEY9dwPv6k3XXWzfYK03URp6rUC3JBmw3Gqu0z6sOqSrYLTrWcKeQKfog7UbEZxVl0KxxhiZff8OAa21odhHt4YA4dYEqgN4CsaDP1k/bAoGAYL1Cledm8aamGrybVkNch/EYjOsaZB6iMwsSVtYaGwAoDCMgi01oIzW+DiDnIgUXkRDz5zenh5Ze0rTFv4bXTZT4dVV/46VDyl44eilXErZQI9mE5p2FeBf2KcPZxre0S9+h2WtyYQDWfo4Pa9b2Bl4ylrWLSybUG+u9pJODj6ECgYB/p4deH7uAXnNSYSy28b5IPD1lFSLqoF3bhSCSyPfKZBZWJ7vSOQVB+SKtLWuCKUAiY8JkMuQSUZB70ZMGekU5K13BmB/SuxDz6m82PX0+p/iP/ePrlUDAzvLm3d/42betiBqC5t0isnmI+vATnFZrjfl6BYc3VAA4HN+RLkIqcwKBgQDINfrpvGqYwNejm4VBZij7ZxJc2vuTBD+XSt+yd4Tk1sZMBS1nKCQAdZwFFun90Q8fjbpNV9ZKeb7TyoOp9Sl4zt3BPU6Mc0ojhr3Le7LOEzlXig+MC3n1zctb4zx7qSlSzt0z0zCIXrDFcDzxjhaAViciGyHgGys1jbjKD3Sqhw==
  -----END RSA PRIVATE KEY-----'''

  # 如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
  # 在windows下，默认生成的txt文件，会有两个问题
  # 1、格式不标准
  # 2、编码不正确 windows 默认编码是gbk

  # 实例化应用
  alipay = AliPay(
      appid="2016092400586022",  # 支付宝app的id
      app_notify_url="",  # 回调视图
      app_private_key_string=app_private_key_string,  # 私钥字符
      alipay_public_key_string=alipay_public_key_string,  # 公钥字符
      sign_type="RSA2",  # 加密方法
  )
  # 发起支付
  order_string = alipay.api_alipay_trade_page_pay(
      out_trade_no=order_id,
      total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
      subject="商贸商城",
      return_url="http://127.0.0.1:8000/buyyer/",
      notify_url=None  # 可选, 不填则使用默认notify url
  )

  # 让用户进行支付的支付宝页面网址
  return "https://openapi.alipaydev.com/gateway.do?" + order_string

def page_not_found(request):
    return render_to_response('buyyer/404.html')

def callbackPay(request):
    return HttpResponse("支付成功")

def paymethod(request,num):
    order=Order.objects.get(id=int(num))
    o_num=order.order_num
    o_m = order.total
    url = Pay(o_num,o_m)
    return HttpResponseRedirect(url)
# Create your views here.