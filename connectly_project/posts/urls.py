from django.urls import path
# from . import views
from .views import UserListCreate, PostListCreate, CommentListCreate, UserDetail, PostDetail, CommentDetail
urlpatterns = [
    # User endpoints
    path('users/', UserListCreate.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),

    # Post endpoints
    path('posts/', PostListCreate.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),

    # Comment endpoints
    path('comments/', CommentListCreate.as_view(), name='comment_list_create'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
]