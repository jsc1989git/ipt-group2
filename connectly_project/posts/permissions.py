from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()
    
class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='User').exists()
    
class IsPostAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user    

class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class IsPostOrCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'post'):
            return obj.post.author == request.user
        return False
    
class IsPostAuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.groups.filter(name='Admin').exists():
            return True
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Admin').exists():
            return True
        
        if hasattr(obj, 'author'):
            return obj.author == request.user
        
        return False
    
class IsCommentAuthorOrPostAuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.groups.filter(name='Admin').exists():
            return True
            
        return True
        
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Admin').exists():
            return True
            
        if obj.author == request.user:
            return True
            
        if hasattr(obj, 'post') and obj.post.author == request.user:
            return True
            
        return False
    