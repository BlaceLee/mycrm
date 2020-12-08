import hashlib

from django.shortcuts import (
    render, redirect, HttpResponse
)
from django.conf import settings

from rbac.utils.forms.verify_form import LoginForm
from rbac.models import User
from sales import models
from rbac.utils.Permissions import permissions


def my_md5(value):
    v = value.encode('utf-8')
    m = hashlib.md5()
    m.update(v)
    return m.hexdigest()


# 登录验证,注入权限路由到session
def login(request):
    """
    登录验证,注入权限路由到session
    用户信息需要根据实际情况做相应修改,此userinfo和user为两个不同的,实际情况应该为一张表
    :param request:
    :return:
    """
    if request.method == "GET":
        login_obj = LoginForm()
        return render(request, 'login.html', {'login_obj': login_obj})
    else:
        login_obj = LoginForm(request.POST)
        if login_obj.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            role_obj = User.objects.filter(name=username).first()
            user_obj = models.UserInfo.objects.filter(username=username).first()
            if username == role_obj.name and password == role_obj.password:
                if user_obj.is_active:
                    request.session['user_id'] = user_obj.id
                    permissions(request, role_obj)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'login_obj': login_obj, 'error': '不存在此用户'})
            else:
                return render(request, 'login.html', {'login_obj': login_obj})

        else:
            return render(request, 'login.html', {'login_obj': login_obj})
