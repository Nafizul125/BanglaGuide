from django import forms
from .models import Car, Booking


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'rent', 'number', 'city', 'main_image']  # add main_image (optional)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
