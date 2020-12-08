from django import forms

from sales import models


# 客户展示
class All_Customers(forms.ModelForm):
    class Meta:
        model = models.Customers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'course':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


# 跟踪记录
class ConsultRecord(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'delete_status':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field == 'customer':
                self.fields[field].queryset = models.Customers.objects.filter(consultant=request.user_obj)
            # elif field == ''


# 报名记录
class Enrollment(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_key, field in self.fields.items():
            if field_key != 'contract_agreed' and field_key != 'delete_status':
                field.widget.attrs.update({'class': 'form-control'})
            if field_key == 'customer':
                field.queryset = models.Customers.objects.filter(consultant=request.user_obj)


# 学习记录
class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = "__all__"


