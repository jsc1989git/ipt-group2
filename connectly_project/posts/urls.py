from django.urls import path
# from . import views
from .views import UserListCreate, PostListCreate, CommentListCreate

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user_list_create'),
    # path('users/get/', views.get_users, name='get_users'),
    # path('users/create/', views.create_user, name='create_user'),
    path('posts/', PostListCreate.as_view(), name='post_list_create'),
    # path('posts/get/', views.get_posts, name='get_posts'),
    # path('posts/create/', views.create_post, name='create_post'),
    path('comments/', CommentListCreate.as_view(), name='comment_list_create')
]