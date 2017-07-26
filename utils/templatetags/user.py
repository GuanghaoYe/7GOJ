# coding=utf-8
import datetime
from account.models import User
from django import template


def get_username(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return ""




register = template.Library()
register.filter("get_username", get_username)

