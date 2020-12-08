import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import (redirect, HttpResponse, render)
from django.urls import reverse
from sales import models


class User_Authe(MiddlewareMixin):
    def process_request(self, request):
        request.cur_id = None
        white_list = [reverse('login'), '/admin/*']

        for path in white_list:
            if re.match(path, request.path):
                request.breadcrumb = None
                return
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        permission_while_list = [reverse('index')]
        for path in permission_while_list:
            if re.match(path, request.path):
                request.breadcrumb = None
                return

        u_name = models.UserInfo.objects.filter(pk=user_id).values('username').first()
        request.user_name = u_name['username']
        request.user_obj = models.UserInfo.objects.filter(pk=user_id).first()
        permission_dict = request.session.get('permission_dict')
        for key, permission in permission_dict.items():
            if re.match(permission['permissions__url'], request.path):
                # pid = permission['permissions__parent_id']
                # if pid:
                #     request.cur_id = pid
                # else:
                request.cur_id = permission.get('permissions__pk')
                request.breadcrumb = {'url': permission.get('permissions__url'),
                                      'title': permission.get('permissions__title')}
                return
            else:
                for p in permission['children']:
                    if re.match(p['permissions__url'], request.path):
                        pid = p['permissions__parent_id']
                        if pid:
                            request.cur_id = pid
                            request.breadcrumb = {'url': permission.get('permissions__url'),
                                                  'title': permission.get('permissions__title'),
                                                  'children': {'url': p['permissions__url'],
                                                               'title': p['permissions__title']}}

                        return
        else:
            return HttpResponse('你无权访问')





