from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.contrib.auth import authenticate, login as signin
from .form import LoginForm


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            user = authenticate(
                username=login_data['username'], password=login_data['password'])
            if user:
                signin(request, user)
                redirect_url = request.GET.get('next') or '/'
                return redirect(redirect_url)
            else:
                login_form.add_error('password', '用户名或密码错误')

        return render(request, 'login.html', {'login_form': login_form})
    else:
        login_form = LoginForm()
        return render(request, 'login.html', locals())
