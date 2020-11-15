from django.db import models

# Create your models here.


class Mobile(models.Model):
    """
    手机

    name 手机名称
    worth_n 值得数量
    not_worth_n 不值得数量
    comment_n 评论数量
    source 来源平台
    """

    name = models.CharField(max_length=255, default='')
    worth_n = models.IntegerField(default=0)
    not_worth_n = models.IntegerField(default=0)
    comment_n = models.IntegerField(default=0)
    source = models.CharField(max_length=255, default='')


class Comment(models.Model):
    """
    评论

    mobile 所属手机
    content 评论内容
    not_worth_n 不值得数量
    comment_n 评论数量
    source 来源平台
    """

    mobile = models.ForeignKey(
        'Mobile',
        on_delete=models.CASCADE,
    )
    content = models.TextField(max_length=1000, default='')
    sentiment = models.DecimalField(max_digits=11, decimal_places=10)
    comment_t = models.DateTimeField()
    create_t = models.DateTimeField()
