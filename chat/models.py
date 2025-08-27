from django.db import models
from django.contrib.auth.models import User  # Use CustomUser if needed

class Post(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.user.name} at {self.timestamp}'

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.user.name} at {self.timestamp}'