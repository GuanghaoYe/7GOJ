# coding=utf-8
from django.db import models

from account.models import User
from group.models import Group
from utils.models import RichTextField
from datetime import datetime


class Announcement(models.Model):
    # 标题
    title = models.CharField(max_length=50)
    # 公告的内容 HTML 格式
    content = RichTextField()
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 这个公告是谁创建的
    created_by = models.ForeignKey(User)
    # 最后更新时间
    last_update_time = models.DateTimeField(auto_now=True)
    # 是否可见 false的话相当于删除
    visible = models.BooleanField(default=True)

    problem_id = models.IntegerField(default=0)

    last_updated_by = models.IntegerField(null=True)

    comment_number = models.IntegerField(default=0)

    priority = models.IntegerField(default=0)

    class Meta:
        db_table = "announcement"

    def add_comment(self, user):
        self.comment_number += 1
        self.last_updated_by = user.id
        self.last_update_time = datetime.now()
        self.save(update_fields=["comment_number", "last_updated_by", "last_update_time"])
