from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, status, filters, permissions
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .factories import PostFactory
from .utils import success_response, error_response
from .singleton import LoggerSingleton
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
import requests
from google.oauth2 import id_token
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'


logger = LoggerSingleton().get_logger()
logger.info("API initialized successfully.")

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return error_response('Token is required.', status_code=status.HTTP_400_BAD_REQUEST)
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
        
        if response.status_code != 200:
            return error_response('Invalid token.', status_code=status.HTTP_400_BAD_REQUEST)
        
        user_info = response.json()
        email = user_info.get('email')

        if not email:
            return error_response('Email not found in user info.', status_code=status.HTTP_400_BAD_REQUEST)
        
        user, created = User.objects.get_or_create(username=email, defaults={'email': email})
        auth_token, _ = Token.objects.get_or_create(user=user)
        return success_response('Login successful', {'token': auth_token.key, 'username': user.username})
    except Exception as e:
        logger.error(f'Google login failed: {str(e)}')
        return error_response('Google login failed.', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return error_response('Username and password are required.', status_code=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return error_response('Username already exists.', status_code=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)

        token, created = Token.objects.get_or_create(user=user)
        return success_response('User registered successfully!', {'token': token.key}, status_code=status.HTTP_201_CREATED)
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend, 
        filters.OrderingFilter
    ]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        post_type = request.data.get('post_type')
        title = request.data.get('title')
        content = request.data.get('content', '')
        metadata = request.data.get('metadata', {})
        author = request.user

        try:
            post = PostFactory.create_post(post_type, title, content, metadata, author)
        except ValueError as e:
            return error_response(str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(post)
        return success_response('Post created successfully!', serializer.data, status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response('Post updated successfully!', serializer.data, status.HTTP_200_OK)
        return error_response('Post update failed.', serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user:
            return error_response('You can only delete your own posts.', status_code=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return success_response('Post deleted successfully!', status_code=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response('Comment created successfully!', serializer.data, status.HTTP_201_CREATED)
        return error_response('Comment creation failed.', serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response('Comment updated successfully!', serializer.data, status.HTTP_200_OK)
        return error_response('Comment update failed.', serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user != instance.author and request.user != instance.post.author:
            return error_response('You do not have permission to delete this comment', status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return success_response('Comment deleted successfully!', status_code=status.HTTP_204_NO_CONTENT)
    
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Like a post
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return error_response('You already liked this post.', status.HTTP_400_BAD_REQUEST)
        
        return success_response('Post liked succesfully!', status_code=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        # Unlike a post
        like = Like.objects.filter(user=request.user, post_id=pk)

        if not like.exists():
            return error_response('Like not found.', status.HTTP_400_BAD_REQUEST)
        
        like.delete()
        return success_response('Post unliked successfully!', status_code=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def likes_count(self, request, pk=None):
        # Get total likes for a post
        count = Like.objects.filter(post_id=pk).count()
        return success_response('Total likes count retrieved', {'likes' : count}, status.HTTP_200_OK)