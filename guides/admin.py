from django.contrib import admin
from .models import Guide

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'division', 'approved')
    list_filter = ('approved', 'division')
    search_fields = ('name', 'email')
    actions = ['approve_guides']

    def approve_guides(self, request, queryset):
        queryset.update(approved=True)
    approve_guides.short_description = "Approve selected guides"