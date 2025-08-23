from django import forms
from .models import Hotel

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'phone_number', 'room_rent', 'facilities', 'rating', 'image']