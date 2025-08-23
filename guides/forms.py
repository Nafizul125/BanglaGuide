from django import forms
from .models import Guide

class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['name', 'email', 'mobile', 'division', 'language']