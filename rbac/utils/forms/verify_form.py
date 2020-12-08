
from django import forms


# 登录
class LoginForm(forms.Form):
    username = forms.fields.CharField(
        label='用户名',
        initial='用户名',
        min_length=3,
        error_messages={'required': '不能为空',
                        'min_length': '长度不得少于3个字符'},
        widget=forms.widgets.TextInput(attrs={
            'placeholder': '用户名',
            'value': '您的用户名',
        })

    )
    password = forms.fields.CharField(
        label='密码',
        initial='密码',
        min_length=5,
        error_messages={'required': '不能为空', 'min_length': '密码太短了'},
        widget=forms.widgets.PasswordInput(attrs={'placeholder': '您的密码'})
    )
