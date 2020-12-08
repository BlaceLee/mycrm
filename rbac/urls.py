from django.conf.urls import url
from rbac.views import verify
from rbac.views import views

urlpatterns = [
	url(r'^login/', verify.login, name='login'),
	# 角色展示
	url(r'^role_show/', views.role_show, name='role_show'),
	# 增加角色
	url(r'^role_add/', views.role_add, name='role_add'),
	# 角色编辑
	url(r'^role_edit/(\d+)', views.role_edit, name='role_edit'),
	# 角色删除
	url(r'^role_del/(\d+)', views.role_del, name='role_del'),
	# 菜单展示
	url(r'^menu_list/', views.menu_list, name='menu_list'),
	# 菜单增加
	url(r'^menu_add/', views.menu_add_edit, name='menu_add'),
	# 菜单编辑
	url(r'^menu_edit/(\d+)/', views.menu_add_edit, name='menu_edit'),
	# 菜单删除
	url(r'^menu_del/(\d+)', views.menu_del, name='menu_del'),
	# 展示各菜单对应的所有权限
	url(r'^show_permissions/(\d+)', views.show_permissions, name='show_permissions'),
	# 批量权限操作
	url(r'^multi_permission/', views.multi_permission, name='multi_permission'),
	# 权限展示
	url(r'^permission_show/', views.permission_show, name='permission_show'),
]