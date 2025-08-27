from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    room_rent = models.TextField()  # e.g., "Single - 3000Tk, Double - 7000Tk"
    facilities = models.TextField()  # Comma-separated or descriptive text
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars, nullable for blank ratings
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)  # Hotel picture
    approved = models.BooleanField(default=False)  # Requires admin approval

    def __str__(self):
        return self.name