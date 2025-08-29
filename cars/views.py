from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Car, Booking
from .forms import CarForm, BookingForm


def _is_provider(user):
    return getattr(user, 'is_service_provider', False)


@login_required
def car_list(request):
    """
    List approved cars with simple search/sort and optional availability filter.
    Query params:
      - query: search text across model/city
      - sort: 'rent_asc' | 'rent_desc' | 'newest'
      - start, end: YYYY-MM-DD strings to filter availability (exclude overlaps)
    """
    cars = Car.objects.filter(approved=True)
    query = request.GET.get('query')
    sort = request.GET.get('sort')
    start = request.GET.get('start')
    end = request.GET.get('end')

    if query:
        cars = cars.filter(Q(model__icontains=query) | Q(city__icontains=query))

    if sort == 'rent_asc':
        cars = cars.order_by('rent', '-created_at')
    elif sort == 'rent_desc':
        cars = cars.order_by('-rent', '-created_at')
    elif sort == 'newest':
        cars = cars.order_by('-created_at')
    else:
        cars = cars.order_by('model')  # default stable order

    # Availability filter: exclude cars with overlapping pending/confirmed bookings
    if start and end:
        cars = cars.exclude(
            bookings__start_date__lt=end,
            bookings__end_date__gt=start,
            bookings__status__in=['pending', 'confirmed'],
        ).distinct()

    return render(request, 'car_list.html', {'cars': cars})


@login_required
def car_add(request):
    if not _is_provider(request.user):
        messages.error(request, 'Only service providers can add cars.')
        return redirect('provider_home')

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)  # accept files
        if form.is_valid():
            car = form.save(commit=False)
            car.approved = False  # pending admin approval
            if hasattr(car, 'owner') and not car.owner_id:
                car.owner = request.user
            car.save()
            messages.success(request, 'Car added. Waiting for admin approval.')
            return redirect('provider_home')
    else:
        form = CarForm()
    return render(request, 'car_add.html', {'form': form})


@login_required
def car_edit(request, pk):
    if not _is_provider(request.user):
        messages.error(request, 'Only service providers can edit cars.')
        return redirect('provider_home')

    car = get_object_or_404(Car, pk=pk)
    if hasattr(car, 'owner_id') and car.owner_id and car.owner_id != request.user.id:
        messages.error(request, 'You can only edit your own cars.')
        return redirect('provider_home')

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)  # accept files
        if form.is_valid():
            car = form.save(commit=False)
            if hasattr(car, 'approved'):
                car.approved = False
            if hasattr(car, 'owner_id') and car.owner_id is None:
                car.owner = request.user
            car.save()
            messages.success(request, 'Car updated. Waiting for admin approval.')
            return redirect('provider_home')
    else:
        form = CarForm(instance=car)
    return render(request, 'car_add.html', {'form': form, 'editing': True, 'car': car})


@login_required
def car_delete(request, pk):
    if not _is_provider(request.user):
        messages.error(request, 'Only service providers can delete cars.')
        return redirect('provider_home')

    car = get_object_or_404(Car, pk=pk)
    if hasattr(car, 'owner_id') and car.owner_id and car.owner_id != request.user.id:
        messages.error(request, 'You can only delete your own cars.')
        return redirect('provider_home')

    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Car deleted.')
        return redirect('provider_home')

    messages.error(request, 'Invalid request.')
    return redirect('provider_home')


@login_required
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk, approved=True)
    form = BookingForm()
    ctx = {'car': car, 'form': form, 'today': timezone.now().date()}
    return render(request, 'car_detail.html', ctx)


@login_required
def book_car(request, pk):
    car = get_object_or_404(Car, pk=pk, approved=True)

    if request.method != 'POST':
        messages.error(request, 'Invalid request.')
        return redirect('car_detail', pk=pk)

    instance = Booking(car=car, user=request.user)
    form = BookingForm(request.POST, instance=instance)

    if form.is_valid():
        booking = form.save(commit=False)
        booking.status = 'pending'
        try:
            booking.save()
        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return redirect('car_detail', pk=pk)

        cart = request.session.get('cart', [])
        found = False
        for item in cart:
            if item.get('type') == 'car' and int(item.get('id', -1)) == car.id:
                item['name'] = car.model
                item['price'] = booking.total_price
                item['start'] = str(booking.start_date)
                item['end'] = str(booking.end_date)
                found = True
                break

        if not found:
            cart.append({
                'type': 'car',
                'id': car.id,
                'name': car.model,
                'price': booking.total_price,
                'start': str(booking.start_date),
                'end': str(booking.end_date),
            })

        request.session['cart'] = cart
        request.session.modified = True

        messages.success(request, f'Booking created (pending). Added to cart: Tk {booking.total_price}.')
        return redirect('cart')

    for field, errs in form.errors.items():
        messages.error(request, f'{field}: {", ".join(errs)}')
    return redirect('car_detail', pk=pk)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    today = timezone.now().date()

    if getattr(booking, 'status', '') == 'cancelled':
        messages.info(request, 'Booking is already cancelled.')
    elif today >= booking.start_date:
        messages.error(request, 'You cannot cancel on/after the start date.')
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')

    return redirect('car_detail', pk=booking.car_id)


@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if not _is_provider(request.user):
        messages.error(request, 'Only providers can confirm bookings.')
        return redirect('provider_home')

    if hasattr(booking.car, 'owner_id') and not (booking.car.owner_id and booking.car.owner_id == request.user.id):
        messages.error(request, 'You can only confirm bookings for your own cars.')
        return redirect('provider_home')

    if getattr(booking, 'status', '') != 'pending':
        messages.error(request, 'Only pending bookings can be confirmed.')
    else:
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'Booking confirmed.')

    return redirect('car_detail', pk=booking.car_id)


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if not _is_provider(request.user):
        messages.error(request, 'Only providers can reject bookings.')
        return redirect('provider_home')

    if hasattr(booking.car, 'owner_id') and not (booking.car.owner_id and booking.car.owner_id == request.user.id):
        messages.error(request, 'You can only reject bookings for your own cars.')
        return redirect('provider_home')

    if getattr(booking, 'status', '') != 'pending':
        messages.error(request, 'Only pending bookings can be rejected.')
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking rejected.')

    return redirect('car_detail', pk=booking.car_id)
