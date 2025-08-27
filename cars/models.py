from django.db import models

class Car(models.Model):
    model = models.CharField(max_length=255)
    rent = models.IntegerField()  # In Tk, without currency symbol
    number = models.CharField(max_length=20)  # Driver number
    city = models.CharField(max_length=100)  # Available city
    approved = models.BooleanField(default=False)  # Requires admin approval

    def __str__(self):
        return self.model