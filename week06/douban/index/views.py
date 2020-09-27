from django.shortcuts import render, HttpResponse

# Create your views here.
from .models import Shorts
from django.http import QueryDict


def index(request):
    # 评分大于3
    conditions = {
        'n_star__gt': 3
    }

    # 获取搜索关键字
    search = request.POST.get('search', '')

    # return HttpResponse(search)

    # 如果有搜索关键字，则增加筛选条件
    if search:
        conditions['short__contains'] = search

    shorts = Shorts.objects.filter(**conditions)

    return render(request, 'index.html', locals())
