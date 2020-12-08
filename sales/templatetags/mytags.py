import re

from django import template
from django.urls import reverse
from django.http.request import QueryDict
from django.conf import settings

register = template.Library()


# 编辑某个页面信息,完成后跳转到当前页
@register.simple_tag
def resolve_url(request, url_name, customer_pk):
    next_url = request.get_full_path()      # 得到编辑前页面路径
    base_url = reverse(url_name, args=(customer_pk,))   # 反向解析编辑路径
    q = QueryDict(mutable=True)     # mutable关键字决定QueryDict对象是否可变,默认False不可变,不能urlencode()
    q['next'] = next_url
    # q.urlencode() 将路径中有&/等特殊字符转换为16进制ascii码值,不做此处理,request.GET.get('next')只能得到&前的键值对
    return base_url + "?" + q.urlencode()


# 权限精确到按钮
@register.filter
def myfilter(request, url_name):
    permission_dict = request.session[settings.PERMISSION_KEY]
    for k, i in permission_dict.items():
        if re.match(i.get('permissions__url'), reverse(url_name)):
            return True
        for p in i['children']:
            if re.match(p.get('permissions__url'), reverse(url_name)):
                return True
    else:
        return False