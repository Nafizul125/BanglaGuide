from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Booking


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'model', 'city', 'rent', 'approved', 'owner', 'created_at')
    list_filter = ('approved', 'city', 'created_at')
    search_fields = ('model', 'city', 'owner__email')
    actions = ['approve_cars']
    readonly_fields = ('image_preview',)

    def approve_cars(self, request, queryset):
        queryset.update(approved=True)
    approve_cars.short_description = "Approve selected cars"

    def thumb(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.main_image.url)
        return "—"
    thumb.short_description = "Image"

    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', obj.main_image.url)
        return "No image uploaded"
    image_preview.short_description = "Preview"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'start_date', 'end_date', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'start_date', 'end_date', 'created_at')
    search_fields = ('car__model', 'car__city', 'user__email')
