from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Task, Category
from .serializers import TaskSerializer, UserSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Task created successfully.'
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Task updated successfully.'
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_completed:
            return Response({'message': 'Cannot delete a completed task.'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'User created successfully.'
        return response