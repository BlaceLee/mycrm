from django.test import TestCase

# Create your tests here.
import os
import hashlib


def myMd5(value):
    v = value.encode('utf-8')
    m = hashlib.md5()
    m.update(v)
    return m.hexdigest()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myorm.settings")
    import django
    django.setup()
    from sales import models
    # models.AdminInfo.objects.create(username='huawei', password=myMd5('123123'))
    models.UserInfo.objects.create(username='vivo', password=myMd5('121212'), is_active=False)
    # models.UserInfo.objects.create(username='huawei', password=myMd5('111111'))
    user_list = []
    for i in range(1, 100):
        obj = models.Customers(qq=str(10000+i), course='Linux')
        user_list.append(obj)
    models.Customers.objects.bulk_create(user_list)

    # class A:
    #     def __init__(self):
    #         self.b = 1
    #
    # a = A()
    # a.c = 2
    # print(a.b, a.c)


