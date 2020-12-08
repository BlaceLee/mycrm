from django.test import TestCase

# Create your tests here.
# import requests
# from bs4 import BeautifulSoup
#
# request = requests.get(url=r'https://fontawesome.dashgame.com/')
# request.encoding = 'utf-8'
# soup = BeautifulSoup(request.text, 'html.parser')
# web = soup.find(attrs={'id': 'web-application'})
# icon_list = []
#
# for item in web.find_all(attrs={'class': 'fa-hover'}):
#     tag = item.find('i')
#     class_name = tag.get('class')[1]
#     icon_list.append([class_name, str(tag)])
#
# print(icon_list)
#
# from sales.urls import urlpatterns
# for i in urlpatterns:
#     print(i)