from rest_framework import serializers
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'is_completed', 'created_at']

def validate_assigned_to(self, value):
    if not User.objects.filter(id=value).exists():
        raise serializers.ValidationError("Assigned user does not exist")
    return value