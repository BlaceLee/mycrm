from django.conf import settings


# menu_list = []


def permissions(request, role_obj):
    permission_list = role_obj.roles.values('permissions__pk',
                                            'permissions__url',
                                            'permissions__title',
                                            'permissions__primary_menus__pk',
                                            'permissions__parent_id',
                                            'permissions__primary_menus__title',
                                            'permissions__primary_menus__icon', ).distinct()
    """
        {
            1:{ title:xxx,
                icon:xx,
                children:[{url:}]
            },
            2: {
                title: yyy,
                icon: yy,
                children:[{'url':xxxx, 'title': yyy]
            }
            }
    """

    permission_dict = {}
    for permission in permission_list:
        if not permission['permissions__parent_id']:
            permission_dict[permission['permissions__pk']] = permission
            permission['children'] = []
        else:
            permission_dict[permission['permissions__parent_id']]['children'].append(permission)

    menu_dict = {}
    for menu in permission_list:
        primary_menu_key = menu.get('permissions__primary_menus__pk')
        if primary_menu_key:
            dic = {
                'title': menu.get('permissions__primary_menus__title'),
                'icon': menu.get('permissions__primary_menus__icon'),
                'children': [{
                    'id': menu.get('permissions__pk'),
                    'url': menu.get('permissions__url'),
                    'title': menu.get('permissions__title'),
                }]
            }
            if not menu_dict.setdefault(primary_menu_key):
                menu_dict[primary_menu_key] = dic
            else:
                menu_dict[primary_menu_key]['children'].append(dic['children'][0])
            # 注入权限和menu
    request.session[settings.PERMISSION_KEY] = permission_dict
    request.session[settings.MENU_KEY] = menu_dict
