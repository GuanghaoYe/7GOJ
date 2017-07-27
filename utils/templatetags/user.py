# coding=utf-8
import datetime
from account.models import User,SUPER_ADMIN
from django import template


def get_username(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return ""

def is_super_admin(user_id):
    try:
        return User.objects.get(id=user_id).admin_type == SUPER_ADMIN
    except User.DoesNotExist:
        return False


register = template.Library()
register.filter("get_username", get_username)
register.filter("is_super_admin",is_super_admin)

