from django.db import models
from django.contrib.auth.models import User
    
class Post(models.Model):
    POST_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=255, default=None) # The title of the post
    content = models.TextField(blank=True) # The text content of the post
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE) # The user who created the post
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text') # The type of post (text, image, video)
    metadata = models.JSONField(default=dict, blank=True) # Additional metadata for the post
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when post is created

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
    
class Comment(models.Model):
    text = models.TextField() # The text content of the comment
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) # The user who created the comment
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # The post the comment belongs to
    created_at = models.DateTimeField(auto_now_add=True) # Timestamp when comment is created

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"