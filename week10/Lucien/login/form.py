from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(label='用户名', required=True, error_messages={'required': '用户名不能为空'},)
    password = forms.CharField(label='密码',widget=forms.PasswordInput, min_length=8, error_messages={'min_length': '密码至少是8位'})
