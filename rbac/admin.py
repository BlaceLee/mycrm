from django.contrib import admin
from rbac import models

# Register your models here.


class PermissionAdim(admin.ModelAdmin):
    list_display = ['id', 'url', 'title', 'primary_menus', 'parent', 'url_name']
    list_editable = ['url', 'title', 'primary_menus', 'parent', 'url_name']


admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Permission, PermissionAdim)
admin.site.register(models.Primary_menu)
