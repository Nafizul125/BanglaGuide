from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'city', 'rent', 'approved')
    list_filter = ('approved', 'city')
    search_fields = ('model', 'city')
    actions = ['approve_cars']

    def approve_cars(self, request, queryset):
        queryset.update(approved=True)
    approve_cars.short_description = "Approve selected cars"