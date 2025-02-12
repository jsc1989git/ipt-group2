from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import TaskViewSet, CategoryViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]