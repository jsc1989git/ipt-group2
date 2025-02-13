from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .factories import PostFactory
from .utils import success_response, error_response

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

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
        self.perform_destroy(instance)
        return success_response('Comment deleted successfully!', status_code=status.HTTP_204_NO_CONTENT)