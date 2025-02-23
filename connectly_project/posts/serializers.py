from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'content': {'allow_blank': True},
        }

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post content cannot be empty.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), error_messages={"does_not_exist": "Post not found."})
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), error_messages={"does_not_exist": "Author not found."})

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'text': {'allow_blank': True},
        }

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'