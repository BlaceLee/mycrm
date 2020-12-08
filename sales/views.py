import hashlib

from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.views import View
from django.db.utils import IntegrityError
from django.forms.models import modelformset_factory

from sales import models
from sales.utils.page import MyPage
from sales import common

from sales.utils.myForm import (
    All_Customers, ConsultRecord, Enrollment, StudyRecordForm)


# Create your views here.


# def my_md5(value):
#     v = value.encode('utf-8')
#     m = hashlib.md5()
#     m.update(v)
#     return m.hexdigest()
#
#
# def login(request):
#     if request.method == "GET":
#         login_obj = LoginForm()
#         return render(request, 'login.html', {'login_obj': login_obj})
#     else:
#         login_obj = LoginForm(request.POST)
#         if login_obj.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             obj = models.UserInfo.objects.filter(username=username).first()
#             if username == obj.username and my_md5(password) == obj.password:
#                 if obj.is_active:
#                     request.session['user_id'] = obj.id
#                     return redirect('all_customers')
#                 else:
#                     return render(request, 'login.html', {'login_obj': login_obj, 'error': '不存在此用户'})
#             else:
#                 return render(request, 'login.html', {'login_obj': login_obj})
#         else:
#             return render(request, 'login.html', {'login_obj': login_obj})

def index(request):
    return render(request, 'index.html')


# def query(fuc, par):
#     if hasattr(common, fuc.strip()):
#         if callable(getattr(common, fuc.strip())):
#             return getattr(common, fuc.strip())(par)


class Customers(View):
    def get(self, request):
        base_url = request.path
        if base_url == reverse('all_customers'):  # 公户
            customer_obj = models.Customers.objects.filter(consultant__username=None)
        else:
            customer_obj = models.Customers.objects.filter(~Q(status='signed'), consultant__username=request.user_name)
            # print(customer_obj)
        customers_key = All_Customers().fields
        per_page_number = 10  # 每页显示数量
        page_tag_number = 5  # 分页显示数量
        cur_page = request.GET.get('page')  # 当前页数
        if not cur_page:
            cur_page = 1
        # customers_total_count = models.Customers.objects.all().count()  # 总数据数
        user_obj = models.UserInfo.objects.all()
        url_par = request.GET.copy()  # queryDict 是不可变的,需要进行深拷贝处理
        field = request.GET.get('op')
        con = request.GET.get('content')
        if field and con:
            # customers_obj = query(field, con)   # 过滤筛选
            # 可以用Q函数实现过滤
            customers_obj = customer_obj.filter(Q(**{field: con}))  # **打散后,为关键字传参
        # customers_obj = models.Customers.objects.filter(Q(**{field: con}))  # **打散后,为关键字传参
        else:
            # customers_obj = models.Customers.objects.all()
            customers_obj = customer_obj
        page_obj = MyPage(cur_page, per_page_number, page_tag_number, customers_obj.count(), base_url, url_par)
        customers_obj = customers_obj.all().order_by('id').reverse()[page_obj.start_html_num:page_obj.end_html_num]

        return render(request, 'all_customers.html',
                      {'customers_obj': customers_obj, 'customers_key': customers_key,
                       "page_obj": page_obj.page_html(), 'user_obj': user_obj,
                       'base_url': base_url})

    def post(self, request):
        op_type = request.POST.get('batch')  # 转换方式
        customer_id = request.POST.getlist('customer_id')
        user_id = request.POST.get('user_id')
        if hasattr(self, op_type):
            obj = models.Customers.objects.filter(id__in=customer_id)
            getattr(self, op_type)(request, obj, user_id)
        return redirect(request.path.strip('/'))

    def public_private(self, request, obj, uid):
        obj.update(consultant_id=uid)

    def private_public(self, request, obj, uid):
        obj.update(consultant=None)


def edit_customer(request, nid=None):
    customer_obj = models.Customers.objects.filter(pk=nid).first()
    if request.method == 'GET':
        customer_form_obj = All_Customers(instance=customer_obj)
        return render(request, 'edit_customer.html', {'customer_form_obj': customer_form_obj, })
    else:
        next_url = request.GET.get('next')  # 取next对应路径,自动将urlencode转换的&/等字符还原
        is_signed = request.POST.get('status')
        if is_signed == 'signed':
            try:
                models.Enrollment.objects.create(customer_id=nid, enrollment_class_id=request.POST.get('class_list'),
                                                 school=models.ClassList.objects.filter(
                                                     pk=request.POST.get('class_list')).first().campuses)
            except IntegrityError:
                return HttpResponse('该用户已经报名该班级了')
        customer_form_obj = All_Customers(request.POST, instance=customer_obj)
        customer_form_obj.save()
        return redirect(next_url)


# 跟进记录
def consult_record(request):
    record_objs = models.ConsultRecord.objects.filter(
        customer__consultant=request.user_obj, delete_status=False)
    cid = request.GET.get('id')
    if cid:
        record_objs = record_objs.filter(customer_id=cid)
    per_page_number = 10  # 每页显示数量
    page_tag_number = 5  # 分页显示数量
    cur_page = request.GET.get('page')  # 当前页数
    if not cur_page:
        cur_page = 1
    url_par = request.GET.copy()
    base_url = request.path
    if request.method == 'GET':
        search_name = request.GET.get('search_name')
        if search_name:
            record_objs = record_objs.filter(customer__name=search_name).order_by('data').reverse()
    else:
        pass
    page_obj = MyPage(cur_page, per_page_number, page_tag_number, record_objs.count(), base_url, url_par)
    record_objs = record_objs.all().order_by('data').reverse()[page_obj.start_html_num:page_obj.end_html_num]
    return render(request, 'consult_record.html', {'record_objs': record_objs, 'page_obj': page_obj.page_html()})


# 增加编辑跟进记录
def add_edit_record(request, nid=None):
    record_objs = models.ConsultRecord.objects.filter(
        customer__consultant=request.user_obj)
    customer_id = request.GET.get('id')
    if nid:  # 编辑时nid有值
        record_obj = record_objs.filter(pk=nid).first()
    elif customer_id:  # 查看某个客户的最新跟进记录
        record_obj = record_objs.filter(customer__id=customer_id).last()
    else:
        record_obj = None
    if request.method == "GET":

        record_forms = ConsultRecord(request, instance=record_obj)
        return render(request, 'add_edit_record.html', {'record_forms': record_forms})
    else:
        record_forms = ConsultRecord(request, request.POST)  # 每次修改跟进记录,则新创建一个记录,如果instance=record_obj,则为更新记录
        record_forms.save()
        return redirect('consult_record')


# 报名记录展示
class EnrollmentView(View):
    def get(self, request):
        enrollment_objs = models.Enrollment.objects.filter(customer__consultant=request.user_obj)
        return render(request, 'enrollment.html', {'enrollment_objs': enrollment_objs})

    def post(self, request):
        pass


# 增加编辑报名记录
def add_edit_enrollment(request, cid=None):
    enrollment_objs = models.Enrollment.objects.filter(customer__consultant=request.user_obj)
    if request.method == "GET":
        if cid:
            enrollment_obj = enrollment_objs.filter(pk=cid).first()
        else:
            enrollment_obj = None
        enrollment_form = Enrollment(request, instance=enrollment_obj)
        return render(request, 'add_edit_enrollment.html', {'enrollmen_forms': enrollment_form})
    else:
        pass


# 课程记录表
class CourseRecordView(View):
    def get(self, request):
        cid = request.GET.get('id')
        if cid:
            create_study_record(cid)
        cur_page = request.GET.get('page')
        if not cur_page:
            cur_page = 1
        base_url = request.path
        per_page_number = 10
        page_tag_number = 5
        url_par = request.GET.copy()
        course_record_objs = models.CourseRecord.objects.all()
        page_obj = MyPage(cur_page, per_page_number, page_tag_number, course_record_objs.count(), base_url, url_par)

        return render(request, 'courserecord.html',
                      {'course_record_objs': course_record_objs, "page_obj": page_obj.page_html()})

    def post(self, request):
        course_ids = request.POST.getlist('course_ids')
        for cid in course_ids:
            create_study_record(cid)
        return redirect('course_record')


# 增加学习记录
def create_study_record(cid):
    course_record_obj = models.CourseRecord.objects.filter(pk=cid).first()
    students = course_record_obj.re_class.customers_set.filter(status='studying')
    study_obj_list = []
    for student in students:
        student_obj = models.StudyRecord(course_record=course_record_obj, student=student)
        study_obj_list.append(student_obj)
    models.StudyRecord.objects.bulk_create(study_obj_list)


# 学习记录展示
class StudyRocordView(View):
    def get(self, request):
        cid = request.GET.get('id')
        if cid:
            study_record_obj = models.StudyRecord.objects.filter(course_record_id=cid)
        else:
            study_record_obj = None
        formset = modelformset_factory(
            model=models.StudyRecord,
            form=StudyRecordForm, extra=0)  # extra指定生成几条待编辑记录
        formset_cls = formset(queryset=study_record_obj)
        return render(request, 'study_record.html', {'formset_cls': formset_cls})

    def post(self, request):
        formset = modelformset_factory(
            model=models.StudyRecord,
            form=StudyRecordForm, extra=0)  # extra指定生成几条待编辑记录
        formset_cls = formset(request.POST)  # 将post数据提交给formset,即各个字段保存有提交的数据
        if formset_cls.is_valid():
            formset_cls.save()
            return redirect(request.path)
        else:
            return render(request, 'study_record.html', {'formset_cls': formset_cls})
