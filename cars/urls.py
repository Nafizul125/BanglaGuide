from django.urls import path
from . import views

urlpatterns = [
    # listings
    path('', views.car_list, name='car_list'),
    path('add/', views.car_add, name='car_add'),
    path('<int:pk>/', views.car_detail, name='car_detail'),
    path('<int:pk>/book/', views.book_car, name='book_car'),

    # NEW: provider management
    path('<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('<int:pk>/delete/', views.car_delete, name='car_delete'),

    # NEW: booking actions
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('booking/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
]
