from rest_framework import serializers
from .models import User, Task, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    class Meta:
        model = Task
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("The task must have a title.")
        return value