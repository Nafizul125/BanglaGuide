from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Car(models.Model):
    model = models.CharField(max_length=255)
    rent = models.IntegerField()  # daily rent in Tk
    number = models.CharField(max_length=20)  # driver contact number
    city = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)  # requires admin approval

    # who owns this listing (provider)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cars",
        null=True, blank=True,
    )

    # sort by newest
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW: one main image per car
    main_image = models.ImageField(upload_to="car_pictures/", blank=True, null=True)

    def __str__(self):
        return self.model

    @property
    def main_image_url(self):
        return self.main_image.url if self.main_image else ""

    class Meta:
        indexes = [
            models.Index(fields=["approved", "city"]),
            models.Index(fields=["-created_at"]),
        ]


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.PositiveIntegerField(default=0)  # in Tk
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=["car", "start_date"]),
            models.Index(fields=["car", "end_date"]),
            models.Index(fields=["status"]),
        ]

    def clean(self):
        # date sanity
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        # Overlap check vs. pending/confirmed bookings for the same car
        overlapping = Booking.objects.filter(
            car=self.car,
            status__in=['pending', 'confirmed'],
            start_date__lt=self.end_date,
            end_date__gt=self.start_date,
        )
        if self.pk:
            overlapping = overlapping.exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This car is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        # Compute total = rent * days
        days = (self.end_date - self.start_date).days
        if days <= 0:
            raise ValidationError("Invalid date range.")
        self.total_price = self.car.rent * days
        self.full_clean()
        super().save(*args, **kwargs)
main_image = models.ImageField(upload_to="car_pictures/", blank=True, null=True)
