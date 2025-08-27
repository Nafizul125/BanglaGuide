"""
banglaguide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import register, user_login, user_logout, provider_register, provider_login, provider_home
from tourism.views import homepage
from hotels.views import hotel_list, hotel_add
from guides.views import guide_list, guide_add
from cars.views import car_list, car_add
from bookings.views import add_to_cart, cart, payment
from chat.views import chat  # New import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('provider_register/', provider_register, name='provider_register'),
    path('login/', user_login, name='login'),
    path('provider_login/', provider_login, name='provider_login'),
    path('homepage/', homepage, name='homepage'),
    path('provider_home/', provider_home, name='provider_home'),
    path('logout/', user_logout, name='logout'),
    path('hotels/', hotel_list, name='hotel_list'),
    path('hotels/add/', hotel_add, name='hotel_add'),
    path('guides/', guide_list, name='guide_list'),
    path('guides/add/', guide_add, name='guide_add'),
    path('cars/', car_list, name='car_list'),
    path('cars/add/', car_add, name='car_add'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('payment/', payment, name='payment'),
    path('chat/', chat, name='chat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)