from django.db import models
from account.models import User
from utils.models import RichTextField


class Comment(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    announcement_id = models.IntegerField()
    content = RichTextField()
    visible = models.BooleanField(default=True)

    class Meta:
        db_table = "comment"
