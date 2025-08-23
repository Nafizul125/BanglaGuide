from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car
from .forms import CarForm

@login_required
def car_list(request):
    cars = Car.objects.filter(approved=True)
    query = request.GET.get('query')
    sort = request.GET.get('sort')

    if query:
        cars = cars.filter(model__icontains=query) | cars.filter(city__icontains=query)

    if sort == 'rent_asc':
        cars = cars.order_by('rent')
    elif sort == 'rent_desc':
        cars = cars.order_by('-rent')

    return render(request, 'car_list.html', {'cars': cars})

@login_required
def car_add(request):
    if not request.user.is_service_provider:
        messages.error(request, 'Only service providers can add cars.')
        return redirect('provider_home')
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.approved = False  # Pending approval
            car.save()
            messages.success(request, 'Car added successfully. Waiting for admin approval.')
            return redirect('provider_home')
    else:
        form = CarForm()
    return render(request, 'car_add.html', {'form': form})