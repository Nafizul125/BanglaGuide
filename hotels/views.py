from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hotel
from .forms import HotelForm

@login_required
def hotel_list(request):
    hotels = Hotel.objects.filter(approved=True)
    query = request.GET.get('query')
    sort = request.GET.get('sort')

    if query:
        hotels = hotels.filter(name__icontains=query)

    if sort == 'rating':
        hotels = hotels.order_by('-rating')  # Descending by rating

    return render(request, 'hotel_list.html', {'hotels': hotels})

@login_required
def hotel_add(request):
    if not request.user.is_service_provider:
        messages.error(request, 'Only service providers can add hotels.')
        return redirect('provider_home')
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.approved = False  # Pending approval
            hotel.save()
            messages.success(request, 'Hotel added successfully. Waiting for admin approval.')
            return redirect('provider_home')
    else:
        form = HotelForm()
    return render(request, 'hotel_add.html', {'form': form})