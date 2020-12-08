from django.contrib import admin


from sales import models
# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['']     # 指定显示字段
    list_editable = ['']      # 指定可编辑字段


admin.site.register(models.UserInfo)  # admin定制化显示
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
admin.site.register(models.Customers)
admin.site.register(models.Department)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)