from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TouristSpot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name