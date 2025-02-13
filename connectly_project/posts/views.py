from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import AllowAny

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]