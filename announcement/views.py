# coding=utf-8
from rest_framework.views import APIView

from django.shortcuts import render
from utils.shortcuts import serializer_invalid_response, error_response, success_response
from comment.models import Comment
from utils.shortcuts import paginate, error_page
from account.models import SUPER_ADMIN, ADMIN
from account.decorators import super_admin_required, login_required
from group.models import Group
from .models import Announcement
from django.core.paginator import Paginator
from .serializers import (CreateAnnouncementSerializer, AnnouncementSerializer,
                          EditAnnouncementSerializer)


@login_required
def announcement_page(request, announcement_id):
    """
    公告的详情页面
    """
    try:
        announcement = Announcement.objects.get(id=announcement_id, visible=True)
    except Announcement.DoesNotExist:
        return error_page(request, u"公告不存在")
    comments = Comment.objects.filter(announcement_id=announcement_id).order_by("create_time").values("create_time",
                                                                                                      "created_by",
                                                                                                      "content")
    return render(request, "oj/announcement/announcement.html", {"announcement": announcement, "comments": comments})


class AnnouncementAdminAPIView(APIView):
    @login_required
    def post(self, request):
        """
        公告发布json api接口
        ---
        request_serializer: CreateAnnouncementSerializer
        """
        serializer = CreateAnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            Announcement.objects.create(title=data["title"], content=data["content"], created_by=request.user)
            return success_response(u"公告发布成功！")
        else:
            return serializer_invalid_response(serializer)

    @login_required
    def put(self, request):
        """
        公告编辑json api接口
        ---
        request_serializer: EditAnnouncementSerializer
        response_serializer: AnnouncementSerializer
        """
        serializer = EditAnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            try:
                announcement = Announcement.objects.get(id=data["id"])
            except Announcement.DoesNotExist:
                return error_response(u"公告不存在")

            announcement.title = data["title"]
            announcement.content = data["content"]
            announcement.visible = data["visible"]
            announcement.save()

            return success_response(AnnouncementSerializer(announcement).data)
        else:
            return serializer_invalid_response(serializer)

    @login_required
    def get(self, request):
        """
        公告分页json api接口
        ---
        response_serializer: AnnouncementSerializer
        """
        announcement = Announcement.objects.all().order_by("-create_time")
        visible = request.GET.get("visible", None)
        if visible:
            announcement = announcement.filter(visible=(visible == "true"))
        return paginate(request, announcement, AnnouncementSerializer)


def announcement_list_page(request, page=1):
    """
    前台的announcemnt列表
    """
    # 正常情况
    announcements = Announcement.objects.filter(visible=True).order_by("-last_update_time")

    # 搜索的情况
    keyword = request.GET.get("keyword", "").strip()
    if keyword:
        announcements = Announcement.filter(Q(title__contains=keyword) | Q(content__contains=keyword)).order_by(
            "-last_update_time")
    paginator = Paginator(announcements, 40)
    try:
        current_page = paginator.page(int(page))
    except Exception:
        return error_page(request, u"不存在的页码")

    previous_page = next_page = None
    try:
        previous_page = current_page.previous_page_number()
    except Exception:
        pass

    try:
        next_page = current_page.next_page_number()
    except Exception:
        pass
    return render(request, "oj/announcement/announcement_list.html",
                  {"announcements": current_page, "page": int(page),
                   "previous_page": previous_page, "next_page": next_page,
                   "keyword": keyword})
