from alipay import AliPay

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
    app_notify_url=None,  # 会掉视图
    app_private_key_string=app_private_key_string,  # 私钥字符
    alipay_public_key_string=alipay_public_key_string,  # 公钥字符
    sign_type="RSA2",  # 加密方法
)
# 发起支付
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="3345416",
    total_amount=str(0.01),  # 将Decimal类型转换为字符串交给支付宝
    subject="商贸商城",
    return_url=None,
    notify_url=None  # 可选, 不填则使用默认notify url
)

# 让用户进行支付的支付宝页面网址
print("https://openapi.alipaydev.com/gateway.do?" + order_string)

