from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_username', 'post_type', 'metadata', 'created_at', 'privacy', 'comments']
        read_only_fields = ['author']
        extra_kwargs = {
            'content': {'allow_blank': True},
            'privacy': {'required': False},
        }

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post content cannot be empty.")
        return value
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), error_messages={"does_not_exist": "Post not found."})
    
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'post', 'author', 'author_username', 'created_at']
        read_only_fields = ['author']
        extra_kwargs = {
            'text': {'allow_blank': True},
        }

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), error_messages={"does_not_exist": "Post not found."})
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), error_messages={"does_not_exist": "User not found."})
    class Meta:
        model = Like
        fields = '__all__'