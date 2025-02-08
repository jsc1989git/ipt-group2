from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True) # User's unique username
    email = models.EmailField(unique=True) # User's unique email
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when user is created

    def __str__(self):
        return self.username
    
class Post(models.Model):
    POST_TYPES = [
        ("blog", "Blog"),
        ("image", "Image"),
        ("video", "Video"),
    ]

    title = models.CharField(max_length=255)  # Add title field
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default="blog")  # Add post_type field
    content = models.TextField(blank=True)  # Content is optional
    metadata = models.JSONField(default=dict, blank=True)  # Store additional post info
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
    
class Comment(models.Model):
    text = models.TextField() # The text content of the comment
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) # The user who created the comment
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # The post the comment belongs to
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when comment is created

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"