# coding=utf-8
from rest_framework.views import APIView

from django.shortcuts import render
from utils.shortcuts import serializer_invalid_response, error_response, success_response
from utils.shortcuts import paginate, error_page
from account.models import SUPER_ADMIN, ADMIN
from account.decorators import super_admin_required
from group.models import Group
from .models import Comment
from announcement.models import Announcement
from .serializers import (CreateCommentSerializer, CommentSerializer)
from account.decorators import login_required


class CommentAdminAPIView(APIView):
    @login_required
    def post(self, request):
        serializer = CreateCommentSerializer(data=request.data)
        # return serializer_invalid_response(serializer)
        if serializer.is_valid():
            data = serializer.data
            Comment.objects.create(announcement_id=data["announcement_id"], content=data["content"],
                                   created_by=request.user)
            announcement = Announcement.objects.get(id=data["announcement_id"])
            announcement.add_comment(request.user)
            return success_response(u"评论发布成功！")
        else:
            return serializer_invalid_response(serializer)

    @login_required
    def get(self, request):
        comment = Comment.objects.all().order_by("create_time")
        visible = request.GET.get("visible", None)
        if visible:
            comment = comment.filter(visible=(visible == "true"))
        return paginate(request, comment, CommentSerializer)
