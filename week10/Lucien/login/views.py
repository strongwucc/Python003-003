from django.shortcuts import render, HttpResponse

# Create your views here.
def login(request):
    if request.method == 'POST':
        return HttpResponse('登录成功')
    else:
        return render(request, 'login.html')