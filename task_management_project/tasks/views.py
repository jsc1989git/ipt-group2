from django.http import JsonResponse
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer

def get_users(request):
    users = list(User.objects.values('id', 'username', 'email', 'created_at'))
    return JsonResponse(users, safe=False)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create(username=data['username'], email=data['email'])
        return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
    
from .models import Task

def get_tasks(request):
    tasks = list(Task.objects.values('id', 'title', 'description', 'is_completed', 'user', 'created_at'))
    return JsonResponse(tasks, safe=False)

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(id=data['user'])
        task = Task.objects.create(title=data['title'], description=data['description'], user=user)
        return JsonResponse({'id': task.id, 'message': 'Task created successfully'}, status=201)
    
class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskListCreate(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)