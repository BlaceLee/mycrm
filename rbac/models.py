from django.db import models


# Create your models here.
# 用户表
class User(models.Model):
    name = models.fields.CharField(max_length=32)
    password = models.fields.CharField(max_length=64, default='123')
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.name


# 角色表
class Role(models.Model):
    name = models.fields.CharField(max_length=32)
    permissions = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name


# 权限表
class Permission(models.Model):
    url = models.fields.CharField(max_length=64)
    title = models.fields.CharField(max_length=32)
    primary_menus = models.ForeignKey('Primary_menu', blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    url_name = models.fields.CharField(max_length=64)

    def __str__(self):
        return self.title


class Primary_menu(models.Model):
    title = models.fields.CharField(max_length=32)

    icon = models.fields.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.title