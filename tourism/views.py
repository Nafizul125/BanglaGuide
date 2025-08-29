# tourism/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .models import District, TouristSpot

@login_required
def homepage(request):
    form = SearchForm(request.GET or None)
    spots = None
    district_name = None

    if form.is_valid() and form.cleaned_data.get('district'):
        district_name = form.cleaned_data['district']
        try:
            district = District.objects.get(name__iexact=district_name)
            spots = TouristSpot.objects.filter(district=district)
        except District.DoesNotExist:
            spots = []
    else:
        # show all spots by default
        spots = TouristSpot.objects.all().order_by('name')

    return render(request, 'homepage.html', {
        'user': request.user,
        'form': form,
        'spots': spots,
        'district_name': district_name,
    })