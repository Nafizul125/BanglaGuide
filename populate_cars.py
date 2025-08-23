from django.conf import settings
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banglaguide.settings')
django.setup()

from cars.models import Car

# Default Cars
cars_data = [
    {
        'model': 'Toyota Axio',
        'rent': 5000,
        'number': '01925478511',
        'city': 'Dhaka'
    },
    {
        'model': 'Toyota Corolla',
        'rent': 6000,
        'number': '01856478590',
        'city': 'Chittagong'
    },
    {
        'model': 'Toyota Premio',
        'rent': 7800,
        'number': '01689457205',
        'city': 'Rajshahi'
    },
    {
        'model': 'Toyota Corolla',
        'rent': 9200,
        'number': '01761557825',
        'city': 'Rangpur'
    },
    {
        'model': 'Toyota Axio',
        'rent': 7300,
        'number': '01645825677',
        'city': 'Khulna'
    },
    {
        'model': 'Alphard',
        'rent': 11500,
        'number': '01355789889',
        'city': 'Chittagong'
    },
    {
        'model': 'X Noah',
        'rent': 12400,
        'number': '01820050090',
        'city': 'Dhaka'
    },
    {
        'model': 'Nissan X-Trail',
        'rent': 14000,
        'number': '01733578899',
        'city': 'Dhaka'
    },
    {
        'model': 'Toyota Axio',
        'rent': 6300,
        'number': '01967892688',
        'city': 'Bogura'
    },
    {
        'model': 'Toyota Premio',
        'rent': 8200,
        'number': '01645783516',
        'city': 'Dhaka'
    },
    {
        'model': 'Toyota Corolla',
        'rent': 6700,
        'number': '01385789215',
        'city': 'Dhaka'
    },
]

# Create cars
for data in cars_data:
    Car.objects.get_or_create(
        model=data['model'],
        defaults=data
    )