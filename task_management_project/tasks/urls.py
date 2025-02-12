from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls