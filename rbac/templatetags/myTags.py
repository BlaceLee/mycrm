from django import template
from django.conf import settings
from django.shortcuts import reverse


register = template.Library()


@register.inclusion_tag('menu.html')
def menu(request):
    menus = request.session.get(settings.MENU_KEY)

    for menu_key, menu_value in menus.items():
        menu_value['display'] = 'display:none'

        for i in menu_value['children']:
            if request.cur_id == i.get('id'):
                i['class'] = 'active'
                menu_value['display'] = 'display:block'
                break

    return {'menus': menus}


@register.inclusion_tag('breadcrumb.html')
def breadcrumb(request):
    breadcrumbs = request.breadcrumb

    return {'breadcrumbs': breadcrumbs}