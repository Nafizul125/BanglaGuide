from django.conf import settings
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banglaguide.settings')
django.setup()

from hotels.models import Hotel

# Default Hotels
hotels_data = [
    {
        'name': 'Hotel Sea Moon',
        'location': "Dolphin circle, Sughandha Beach Rd, Cox's Bazar 4700",
        'phone_number': '01942-828083',
        'room_rent': 'Single - 3000Tk, Double - 7000Tk',
        'facilities': 'Swimming Pool, Free WiFi, Fitness centre, 24-hour front desk, Free parking, Good breakfast',
        'rating': 3
    },
    {
        'name': 'Ramada',
        'location': "Dolphin circle, Cox's Bazar",
        'phone_number': '01896-100012',
        'room_rent': 'Single - 4500Tk, Double - 10000Tk',
        'facilities': 'Bar, Spa, Good breakfast, Swimming Pool, Free WiFi, Fitness centre, 24-hour front desk, Free parking',
        'rating': 5
    },
    {
        'name': 'Hotel Naz Garden',
        'location': 'Bogra City Bypass, Bogura 5800',
        'phone_number': '01755-661199',
        'room_rent': 'Single - 4000Tk, Double - 8500Tk',
        'facilities': 'Swimming Pool, Bar, Free WiFi, 24-hour front desk',
        'rating': 4
    },
    {
        'name': 'Hotel Rattri Nibash',
        'location': 'Mohakhail, Dhaka',
        'phone_number': '01711258956',
        'room_rent': 'Single - 1000Tk, Double - 2000Tk',
        'facilities': 'Free Wifi',
        'rating': None  # Blank rating
    },
    {
        'name': 'Le Méridien Dhaka',
        'location': '79/A Commercial Area Road, Dhaka 1229',
        'phone_number': '09638-900089',
        'room_rent': 'Single - 7000Tk, Double - 15000Tk',
        'facilities': 'Bar, Spa, Swimming Pool, Free parking, Free WiFi, Fitness centre, 24-hour front desk, breakfast',
        'rating': 5
    },
    {
        'name': 'Hotel Noorjahan Grand',
        'location': 'Waves 1 Dargah Gate, Sylhet 3100',
        'phone_number': '01930-111666',
        'room_rent': 'Single - 1200Tk, Double - 2886Tk',
        'facilities': 'Child-friendly, Breakfast buffet, Room service, Pool',
        'rating': 2
    },
]

# Create hotels
for data in hotels_data:
    Hotel.objects.get_or_create(
        name=data['name'],
        defaults=data
    )