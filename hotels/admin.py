from django.contrib import admin
from .models import Hotel

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number', 'rating', 'approved')
    list_filter = ('approved',)
    search_fields = ('name', 'location')
    actions = ['approve_hotels']

    def approve_hotels(self, request, queryset):
        queryset.update(approved=True)
    approve_hotels.short_description = "Approve selected hotels"