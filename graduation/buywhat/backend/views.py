from django.shortcuts import render
from .models import Mobile, Comment

# Create your views here.
def mobile(request):

    mobiles = Mobile.objects.all()

    return render(request, 'mobile.html', locals())

def comment(request, mobile_id):

    mobile = Mobile.objects.get(id=mobile_id)

    comment_conditions = {'mobile_id': mobile_id}

    search_key = request.POST.get('search_key', '')
    start_time = request.POST.get('start_time', '')
    end_time = request.POST.get('end_time', '')

    if search_key:
        comment_conditions['content__contains'] = search_key

    if start_time:
        comment_conditions['comment_t__gte'] = start_time.replace('T', ' ', 1)

    if end_time:
        comment_conditions['comment_t__lte'] = end_time.replace('T', ' ', 1)

    comments = Comment.objects.filter(**comment_conditions)

    return render(request, 'comment.html', locals())
