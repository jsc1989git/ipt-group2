from django.urls import path
from . import views
from .views import UserListCreate, TaskListCreate

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('tasks/', views.get_tasks, name='get_tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('users/', UserListCreate.as_view(), name='user_list_create'),
    path('tasks/', TaskListCreate.as_view(), name='task_list_create')
]