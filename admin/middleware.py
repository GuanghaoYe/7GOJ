# coding=utf-8
import json

from django.http import HttpResponse, HttpResponseRedirect


def is_admin_request(path):
    if path.startswith("/api/admin/upload_image") or path.startswith("/api/admin/announcement/"):
        return False
    if path.startswith("/admin/") or path.startswith("/api/admin"):
        return True

class AdminRequiredMiddleware(object):
    def process_request(self, request):
        path = request.path_info
        if path.startswith("/admin/") or path.startswith("/api/admin/"):
            if not(request.user.is_authenticated() and request.user.admin_type):
                if request.is_ajax():
                    return HttpResponse(json.dumps({"code": 1, "data": u"请先登录"}),
                                        content_type="application/json")
                else:
                    return HttpResponseRedirect("/login/")