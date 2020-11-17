from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.mobile, name='mobile'),
    path('comment/<int:mobile_id>', views.comment, name='comment'),
]
