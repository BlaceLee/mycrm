from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.

source_type = (('qq', 'qq群'),
               ('referral', '内部转介绍'),
               ('website', '官方网站'),
               ('baidu_ads', '百度推广'),
               ('offical_direct', '直接上门'),
               ('WoM', '口碑'),
               ('public_class', '公开课'),
               ('others', '其他'),)

course_type = (('Linux', 'Linux中高级'),
               ('PythonFullStack', 'Python高级全栈开发'),)

status_type = (('signed', '已报名'),
               ('unregistered', '未报名'),
               ('studying', '学习中'),
               ('paid_in_full', '学费已交齐'))

class_type = (('fulltime', '脱产班'),
              ('online', '网络班'),
              ('weekend', '周末班'))

seek_status_choices = (("A", '近期无报名计划'),
                       ("B", '1月内报名'),
                       ("C", '2周内报名'),
                       ("D", '1周内报名'),
                       ("E", '交定金'),
                       ("F", '已到班'),
                       ("G", '付全款'),
                       ("H", '无效'),
                       )

attendance_choices = (('checked', '已签到'),
                      ('vacate', '请假'),
                      ('late', '迟到'),
                      ('absent', '缺勤'),
                      ('leave_early', '早退'),
                      )

score_choices = ((100, 'A+'),
                 (90, 'A'),
                 (85, 'B+'),
                 (80, 'B'),
                 (70, 'B-'),
                 (60, 'C+'),
                 (50, 'C'),
                 (40, 'C-'),
                 (0, 'D'),
                 (-1, 'N/A'),
                 )


# 管理员信息表
class AdminInfo(models.Model):
    username = models.fields.CharField(max_length=32)
    password = models.fields.CharField(max_length=32)


# 用户信息表
class UserInfo(models.Model):
    """
    用户表: 销售/讲师/班主任...
    """
    username = models.fields.CharField(max_length=32)
    password = models.fields.CharField(max_length=32)
    email = models.fields.EmailField()
    telephone = models.fields.CharField(max_length=16)
    is_active = models.fields.BooleanField(default=True)
    department = models.ForeignKey('Department', verbose_name='所属部门', default=1)

    def __str__(self):
        return self.username


"""
如果在已经创建好的表中添加新的外键关系,需要给外键对应的表创建记录,再给外键设置default值
"""


# 部门表
class Department(models.Model):
    """
    部门表
    """
    name = models.fields.CharField('部门', max_length=32)
    count = models.fields.IntegerField('部门人数')

    def __str__(self):
        return self.name


# 客户表
class Customers(models.Model):
    """
    客户表:
    """
    qq = models.fields.CharField(verbose_name="QQ", max_length=32,
                                 unique=True, help_text="QQ号必须唯一")
    qq_name = models.fields.CharField("QQ昵称", max_length=32,
                                      blank=True, null=True)  # blank为True表示在输入时可以为空,null为True表示在mysql中存数据时可以为空
    name = models.fields.CharField("姓名", max_length=32, blank=True, null=True, help_text='学员报名后,需修改为真实姓名')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.fields.CharField("性别", choices=sex_type, max_length=16,
                                  default='male', blank=True, null=True)
    birthday = models.fields.DateField('出生日期', default=None, help_text='格式yyyy-mm-dd', blank=True, null=True)
    phone = models.fields.CharField('手机号', max_length=16, blank=True, null=True)
    source = models.fields.CharField('客户来源', max_length=32, choices=source_type, default='qq')
    introduce_from = models.ForeignKey('self', verbose_name='转介绍自学员',  # self 指的是自己这个表,可以用customers代替
                                       blank=True, null=True, on_delete=models.CASCADE)
    course = MultiSelectField('咨询课程', choices=course_type)
    customer_note = models.fields.TextField('客户备注', blank=True, null=True)
    status = models.fields.CharField('状态', choices=status_type, max_length=32, default='unregistered',
                                     help_text="选择客户此时的状态")
    date = models.fields.DateField('咨询日期', auto_now_add=True)
    last_consult_date = models.fields.DateField('最后跟进日期', auto_now_add=True)
    next_date = models.fields.DateField('预计再次跟进时间', blank=True, null=True)
    class_list = models.ManyToManyField('ClassList', verbose_name='已报班级')

    consultant = models.ForeignKey('UserInfo', verbose_name='销售', related_name='customers',  # related_name字段用于多表查询时反向查询
                                   blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '暂未填写'


# 校区表
class Campuses(models.Model):
    """
    校区表
    """
    name = models.fields.CharField(verbose_name='校区', max_length=64)
    address = models.fields.CharField('详细地址', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name


# 班级表
class ClassList(models.Model):
    course = models.fields.CharField('课程名称', max_length=32, choices=course_type)
    semester = models.fields.IntegerField('学期')
    campuses = models.ForeignKey('Campuses', verbose_name='校区', on_delete=models.CASCADE)
    price = models.fields.IntegerField('学费', default=10000)
    memo = models.fields.CharField('说明', blank=True, null=True, max_length=100)
    start_date = models.fields.DateField('开办日期')
    graduate_date = models.fields.DateField('结业日期', blank=True, null=True)
    teachers = models.ManyToManyField('UserInfo', verbose_name='老师')
    class_type = models.fields.CharField(choices=class_type, max_length=32, verbose_name='班级及类型', blank=True, null=True)

    class Meta:
        unique_together = ('course', 'semester', 'campuses')  # 联合主键

    def __str__(self):
        return self.course


# 跟进记录表
class ConsultRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customers', verbose_name='咨询的客户')
    note = models.fields.TextField(verbose_name='跟进内容')
    status = models.CharField('跟进状态', max_length=8,
                              choices=seek_status_choices, help_text='选择客户此时的状态')
    data = models.fields.DateTimeField('跟进日期', auto_now_add=True)
    delete_status = models.fields.BooleanField(verbose_name='删除状态', default=False)  # 为True只是不显示,但是数据库中仍有记录

    def __str__(self):
        return self.customer.name + ":" + self.data.strftime('%Y-%m-%d %X')


# 报名记录表
class Enrollment(models.Model):
    """
    报名记录表
    """
    customer = models.ForeignKey('Customers', verbose_name='客户名称')
    enrollment_class = models.ForeignKey('ClassList', verbose_name='所属班级')
    school = models.ForeignKey('Campuses', verbose_name='所属学校')
    enrollment_date = models.fields.DateTimeField(verbose_name='报名日期', auto_now_add=True)
    delete_status = models.fields.BooleanField(verbose_name='删除状态', default=False)
    memo = models.fields.TextField('备注', blank=True, null=True)
    why_us = models.fields.TextField('为什么报名', max_length=1024, blank=True, null=True, default=None)
    your_expectation = models.TextField('你的期望', max_length=1024, blank=True, null=True, default=None)
    contract_agreed = models.BooleanField('我已认真阅读完培训协议并同意全部协议内容', default=False)

    class Meta:
        unique_together = ('customer', 'enrollment_class')


# 课程记录表
class CourseRecord(models.Model):
    """课程记录表"""
    day_num = models.fields.IntegerField('节次', help_text='此处填写第几节课或第几天课程...,必须为数字')
    date = models.DateField('上课日期', auto_now_add=True)
    course_title = models.fields.CharField('课程标题', max_length=64, blank=True, null=True)
    course_memo = models.fields.TextField('课程内容', max_length=1024, blank=True, null=True)
    has_homework = models.BooleanField('本节有作业', default=True)
    homework_title = models.TextField('作业标题', max_length=1024, blank=True, null=True)
    homework_memo = models.TextField('作业描述', max_length=512, blank=True, null=True)
    scoring_point = models.TextField('得分点', max_length=128, blank=True, null=True)
    re_class = models.ForeignKey('ClassList', verbose_name='班级')
    teacher = models.ForeignKey('UserInfo', verbose_name='讲师')

    class Meta:
        unique_together = ('re_class', 'day_num')

    def __str__(self):
        return str(self.day_num) + ':' + self.course_title


# 学习记录表
class StudyRecord(models.Model):
    """学习记录表"""
    attendance = models.CharField('考勤', choices=attendance_choices, default='checked', max_length=64)
    score = models.IntegerField('本节成绩', choices=score_choices, default=-1)
    homework_note = models.CharField('作业批语', max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField('备注', max_length=128, blank=True, null=True)
    homework = models.FileField(verbose_name="作业文件", blank=True, null=True, default=None)
    course_record = models.ForeignKey('CourseRecord', verbose_name='课程')
    student = models.ForeignKey('Customers', verbose_name='学员')

    class Meta:
        unique_together = ('course_record', 'student')

    def __str__(self):
        return self.student