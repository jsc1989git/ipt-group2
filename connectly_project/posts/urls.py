from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
from .views import PostViewSet, CommentViewSet, LikeViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('auth/google/login/', views.google_login, name='google_login'),
]