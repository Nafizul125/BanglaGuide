from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hotels.models import Hotel
from guides.models import Guide
from cars.models import Car
from django.contrib import messages
import requests
from datetime import datetime, timedelta
from django.conf import settings
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        item_type = request.POST.get('type')
        item_id = request.POST.get('id')
        cart = request.session.get('cart', [])

        # Check if already in cart
        for item in cart:
            if item['type'] == item_type and item['id'] == int(item_id):
                return JsonResponse({'status': 'already_added'})

        if item_type == 'hotel':
            hotel = Hotel.objects.get(id=item_id)
            single_price, double_price = parse_hotel_prices(hotel.room_rent)
            cart.append({'type': 'hotel', 'id': hotel.id, 'name': hotel.name, 'single_qty': 0, 'double_qty': 0, 'single_price': single_price, 'double_price': double_price})
        elif item_type == 'guide':
            guide = Guide.objects.get(id=item_id)
            cart.append({'type': 'guide', 'id': guide.id, 'name': guide.name, 'price': 1200})
        elif item_type == 'car':
            car = Car.objects.get(id=item_id)
            cart.append({'type': 'car', 'id': car.id, 'name': car.model, 'price': car.rent})

        request.session['cart'] = cart
        return JsonResponse({'status': 'added'})
    return JsonResponse({'status': 'error'})

@login_required
def cart(request):
    cart = request.session.get('cart', [])
    total = 0
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    weather = None

    if start_date and end_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        nights = (end_dt - start_dt).days
        if nights < 1:
            nights = 1
        # Check if date is within 5-day forecast window from today (August 22, 2025)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).date()
        if (start_dt.date() - today).days > 5 or (start_dt.date() - today).days < 0:
            weather = "Weather data unavailable (outside 5-day forecast)"
        else:
            weather = get_weather('Dhaka', start_date)  # Assume Dhaka

    for item in cart:
        if item['type'] == 'hotel':
            hotel_total = (item['single_qty'] * item['single_price'] + item['double_qty'] * item['double_price']) * (nights if start_date else 1)
            item['subtotal'] = hotel_total
            total += hotel_total
        else:
            item['subtotal'] = item['price']
            total += item['price']

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_dates':
            request.session['start_date'] = request.POST.get('start_date')
            request.session['end_date'] = request.POST.get('end_date')
            return redirect('cart')
        elif action == 'update_qty':
            index = int(request.POST.get('index'))
            single_qty = int(request.POST.get('single_qty', 0))
            double_qty = int(request.POST.get('double_qty', 0))
            cart[index]['single_qty'] = max(0, single_qty)  # Prevent negative
            cart[index]['double_qty'] = max(0, double_qty)
            request.session['cart'] = cart
            return JsonResponse({'status': 'updated'})

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).date()
    future_date = today + timedelta(days=5)
    return render(request, 'cart.html', {'cart': cart, 'total': total, 'start_date': start_date, 'end_date': end_date, 'weather': weather, 'today': today, 'future_date': future_date})

@login_required
def payment(request):
    cart = request.session.get('cart', [])
    total = 0
    for item in cart:
        if item['type'] == 'hotel':
            nights = (datetime.strptime(request.session['end_date'], '%Y-%m-%d') - datetime.strptime(request.session['start_date'], '%Y-%m-%d')).days
            hotel_total = (item['single_qty'] * item['single_price'] + item['double_qty'] * item['double_price']) * nights
            total += hotel_total
        else:
            total += item['price']

    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')
        if payment_option:
            messages.success(request, 'Thank You For Your Payment.')
            request.session['cart'] = []
            request.session.pop('start_date', None)
            request.session.pop('end_date', None)
            return redirect('homepage')

    return render(request, 'payment.html', {'cart': cart, 'total': total})

def get_weather(city, date):
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        for forecast in data['list']:
            forecast_date = datetime.fromtimestamp(forecast['dt']).date()
            if forecast_date == target_date:
                return {
                    'temp': forecast['main']['temp'],
                    'condition': forecast['weather'][0]['main']
                }
        logger.warning(f"No weather data found for {date}")
        return "No weather data available for this date"
    except requests.RequestException as e:
        logger.error(f"Weather API error: {e}")
        return "Weather API error"

def parse_hotel_prices(room_rent):
    # Parse "Single - 3000Tk, Double - 7000Tk"
    parts = room_rent.split(',')
    single = int(parts[0].split('-')[1].strip().replace('Tk', ''))
    double = int(parts[1].split('-')[1].strip().replace('Tk', ''))
    return single, double