require(["jquery", "avalon", "csrfToken", "bsAlert", "validator", "pager", "editorComponent"],
    function ($, avalon, csrfTokenHeader, bsAlert, editor) {
        avalon.ready(function () {

            if (avalon.vmodels.comment){
                var vm = avalon.vmodels.comment;
            }
            else {
                var vm = avalon.define({
                    $id: "comment",
                    commentList: [],
                    isEditing: false,
                    showVisibleOnly: false,

                    //编辑器同步变量
                    commentId: -1,
                    commentVisible: false,

                    pager: {
                        getPage: function(page){
                            getPage(page);
                        }
                    },

                    createCommentEditor: {
                        editorId: "create-comment-editor",
                        placeholder: "内容"
                    },

                    editCommentEditor: {
                        editorId: "edit-comment-editor",
                        placeholder: "内容"
                    },

                    editComment: function (comment) {
                        vm.commentId = comment.id;
                        avalon.vmodels.editCommentEditor.content = comment.content;
                        vm.comment = comment.visible;
                        vm.isEditing = true;
                    },
                    cancelEdit: function () {
                        vm.isEditing = false;
                    },
                    submitChange: function () {
                        var content = avalon.vmodels.editCommentEditor.content;

                        if (content == "") {
                            bsAlert("内容不能为空");
                            return false;
                        }

                        $.ajax({
                            url: "/api/admin/comment/",
                            contentType: "application/json;charset=UTF-8",
                            dataType: "json",
                            method: "put",
                            data: JSON.stringify({
                                id: vm.commentId,
                                content: content,
                                visible: vm.commentVisible
                            }),
                            success: function (data) {
                                if (!data.code) {
                                    bsAlert("修改成功");
                                    vm.isEditing = false;
                                    getPage(1);
                                }
                                else {
                                    bsAlert(data.data);
                                }
                            }
                        });

                    }
                });

                vm.$watch("showVisibleOnly", function () {
                    getPage(1);
                    avalon.vmodels.commentcurrentPage = 1;
                });
            }

            function getPage(page) {
                var url = "/api/admin/comment/?paging=true&page=" + page + "&page_size=20";
                if (vm.showVisibleOnly)
                    url += "&visible=true";
                $.ajax({
                    url: url,
                    method: "get",
                    success: function (data) {
                        if (!data.code) {
                            vm.commentList = data.data.results;
                            avalon.vmodels.commentPager.totalPage = data.data.total_page;
                        }
                        else {
                            bsAlert(data.data);
                        }
                    }
                });
            }

            //新建公告表单验证与数据提交
             $("#comment-form").validator().on('submit', function (e) {
                if (!e.isDefaultPrevented()) {
                    var content = avalon.vmodels.createCommentEditor.content;
                    var announcementId = location.pathname.split("/")[2];
                    if (content == "") {
                        bsAlert("请填写公告内容");
                        return false;
                    }
                    $.ajax({
                        beforeSend: csrfTokenHeader,
                        url: "/api/admin/comment/",
                        contentType: "application/json",
                        data: JSON.stringify({
                            content: content,
                            announcement_id:announcementId
                        }),
                        dataType: "json",
                        method: "post",
                        success: function (data) {
                            if (!data.code) {
                                bsAlert("提交成功！");
                                avalon.vmodels.createCommentEditor.content = "";
                                getPage(1);
                            } else {
                                bsAlert(data.data);
                            }
                        }
                    });
                    return false;
                }
            })
        });
        avalon.scan();
    });
