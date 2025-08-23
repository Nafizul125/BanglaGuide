from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .models import District, TouristSpot

@login_required
def homepage(request):
    form = SearchForm(request.GET or None)
    spots = None
    district_name = None

    if form.is_valid():
        district_name = form.cleaned_data['district']
        try:
            district = District.objects.get(name__iexact=district_name)
            spots = TouristSpot.objects.filter(district=district)
        except District.DoesNotExist:
            spots = []  # No district found, show empty list

    return render(request, 'homepage.html', {
        'user': request.user,
        'form': form,
        'spots': spots,
        'district_name': district_name,
    })