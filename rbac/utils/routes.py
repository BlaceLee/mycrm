
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls.resolvers import RegexURLResolver, RegexURLPattern

from collections import OrderedDict


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    # 是否路由中还有include
    for item in urlpatterns:
        if isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = f'{pre_namespace}:{item.namespace}'
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)
        else:
            if pre_namespace:
                url_name = f'{pre_namespace}:{item.name}'
            else:
                url_name = item.name

            if not item.name:
                raise Exception('URL中必须设置name属性')

            url = pre_url + item._regex  # item._regex 获取url路由中路径[r'^login/', views.login, name='login']中的^login/
            url_ordered_dict[url_name] = {'url_name': url_name, 'url': url.replace('^', '').replace('$', '')}


def get_all_url_dict(ignore_namespace_list=None):
    ignore_list = ignore_namespace_list or []
    url_ordered_dict = OrderedDict()

    md = import_string(settings.ROOT_URLCONF)
    urlpatterns = []

    for item in md.urlpatterns:
        if isinstance(item, RegexURLResolver) and item.namespace in ignore_list:
            continue
        urlpatterns.append(item)
    recursion_urls(None, '/', urlpatterns, url_ordered_dict)
    return url_ordered_dict