from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.contrib.auth import authenticate, login as signin
from .form import LoginForm


def login(request):
    if request.method == 'POST':
        # return HttpResponse('登录成功')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            user = authenticate(
                username=login_data['username'], password=login_data['password'])
            if user:
                signin(request, user)
                return redirect('/home/hello')
            else:
                return HttpResponse('用户名或密码错误')
        else:
            return HttpResponse('登录失败')
    else:
        login_form = LoginForm()
        return render(request, 'login.html', locals())
