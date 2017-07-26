from rest_framework import serializers
from account.models import User
from .models import Comment


class CreateCommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=10000)
    announcement_id = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ["username"]

    created_by = UserSerializer()

    class Meta:
        model = Comment
