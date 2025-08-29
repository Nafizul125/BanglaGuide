from django.conf import settings
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banglaguide.settings')
django.setup()

from guides.models import Guide

# Default Guides
guides_data = [
    {
        'name': 'Md Shajedur Rahaman Sajol',
        'email': 'm.sajolbd@gmail.com',
        'mobile': '+8801710774782',
        'division': 'Dhaka',
        'language': 'Bangla'
    },
    {
        'name': 'Mostafizur Rahman Jewel',
        'email': 'luckypseven@gmail.com',
        'mobile': '01714075718',
        'division': 'Chittagong',
        'language': 'Bangla English'
    },
    {
        'name': 'KHUSBU KHALIL MIMI',
        'email': 'khusbumimi2018@gmail.com',
        'mobile': '01990931420',
        'division': 'Rajshahi',
        'language': 'Bangla, English, Spanish.'
    },
    {
        'name': 'Syed Mahbubul Islam Bulu',
        'email': 'info@riveraintour.com',
        'mobile': '01712292871',
        'division': 'Rangpur',
        'language': 'Bangla, English'
    },
    {
        'name': 'Syed Shafat Uddin Ahmed Tomal',
        'email': 'sales@marketn-trance.com',
        'mobile': '01944455566',
        'division': 'Sylhet',
        'language': 'English, Spanish, Bangla'
    },
    {
        'name': 'MD MONIRUZZAMAN MASUM',
        'email': 'windowmasum@gmail.com',
        'mobile': '+8801841152000',
        'division': 'Mymensingh',
        'language': 'Bangla, English'
    },
    {
        'name': 'Md. Mostafizur Rahman',
        'email': 'lastdaytrips@gmail.com',
        'mobile': '+8801791005909',
        'division': 'Dhaka',
        'language': 'Bangla, English, Spanish'
    },
    {
        'name': 'Masudur Rahman',
        'email': 'cpaid143@gmail.com',
        'mobile': '01736145637',
        'division': 'Rajshahi',
        'language': 'Bangla'
    },
    {
        'name': 'MD KHALILUR RAHMAN',
        'email': 'mdkr1983@gmail.com',
        'mobile': '01911591114',
        'division': 'Chittagong',
        'language': 'Bangla, English, Spanish'
    },
    {
        'name': 'Remon',
        'email': 'remonrex@gmail.com',
        'mobile': '01862825778',
        'division': 'Khulna',
        'language': 'Bangla, English'
    },
    {
        'name': 'Md. Ashiqur Rahman Bhuia',
        'email': 'aashiqq951@gmail.com',
        'mobile': '+8801949091478',
        'division': 'Sylhet',
        'language': 'Bangla, English'
    },
    {
        'name': 'Roknuzzaman',
        'email': 'ro.poros@yahoo.com',
        'mobile': '+8801938771081',
        'division': 'Dhaka',
        'language': 'Bangla, English'
    },
    {
        'name': 'JAWAD MUSTAKIM',
        'email': 'jawad.mustakim02@gmail.com',
        'mobile': '01927294977',
        'division': 'Khulna',
        'language': 'Bangla'
    },
    {
        'name': 'M.A. Siddique Antor',
        'email': 'antor2548@gmail.com',
        'mobile': '01785190256',
        'division': 'Barishal',
        'language': 'Bangla, English'
    },
]

# Create guides
for data in guides_data:
    Guide.objects.get_or_create(
        name=data['name'],
        defaults=data
    )