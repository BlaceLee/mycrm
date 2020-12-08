from django.conf.urls import url
from sales import views

urlpatterns = [
    # url(r'^login/', views.login, name='login'),
    # 信息显示请求
    # url(r'^all_customers/', views.all_customers, name='all_customers'),
    # 首页
    url(r'^index/', views.index, name='index'),
    # 信息显示请求
    url(r'^all_customers/', views.Customers.as_view(), name='all_customers'),
    # 显示我的客户
    url(r'^my_customers/', views.Customers.as_view(), name='my_customers'),
    # 增加编辑客户信息
    url(r'^edit_customer/(\d+)? ', views.edit_customer, name='edit_customer'),
    # # 筛选
    # url(r'^query/ ', views.query, name='query'),
    # 跟进记录
    url(r'^consult_record/', views.consult_record, name='consult_record'),
    # 增加编辑跟进记录
    url(r'^add_edit_record/(\d+)?', views.add_edit_record, name='add_edit_record'),
    # 报名记录
    url(r'^enrollment/', views.EnrollmentView.as_view(), name='enrollment'),
    # 增加编辑报名记录
    url(r'^add_edit_enrollment/(\d+)?/', views.add_edit_enrollment, name='add_edit_enrollment'),
    # 课程记录
    url(r'^course_record/', views.CourseRecordView.as_view(), name='course_record'),
    # 学习记录
    url(r'^study_record/', views.StudyRocordView.as_view(), name='study_record'),


]
