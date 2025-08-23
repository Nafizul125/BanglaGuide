from django.db import models

class Guide(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    division = models.CharField(max_length=100)
    language = models.CharField(max_length=255)  # e.g., "Bangla, English, Spanish"
    approved = models.BooleanField(default=False)  # Requires admin approval

    def __str__(self):
        return self.name