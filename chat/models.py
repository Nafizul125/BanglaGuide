from django.db import models

class Post(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        uname = (getattr(self.user, "name", None) or getattr(self.user, "username", None)) if self.user else "Guest"
        return f'Post by {uname} at {self.timestamp}'

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        uname = (getattr(self.user, "name", None) or getattr(self.user, "username", None)) if self.user else "Guest"
        return f'Reply by {uname} at {self.timestamp}'
