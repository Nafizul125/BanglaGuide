from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Guide
from .forms import GuideForm

@login_required
def guide_list(request):
    guides = Guide.objects.filter(approved=True)
    query = request.GET.get('query')
    sort = request.GET.get('sort')
    language = request.GET.get('language')

    if query:
        guides = guides.filter(name__icontains=query)

    if language:
        guides = guides.filter(language__icontains=language)

    if sort == 'division':
        guides = guides.order_by('division')

    return render(request, 'guide_list.html', {'guides': guides})

@login_required
def guide_add(request):
    if not request.user.is_service_provider:
        messages.error(request, 'Only service providers can add guides.')
        return redirect('provider_home')
    if request.method == 'POST':
        form = GuideForm(request.POST)
        if form.is_valid():
            guide = form.save(commit=False)
            guide.approved = False  # Pending approval
            guide.save()
            messages.success(request, 'Guide added successfully. Waiting for admin approval.')
            return redirect('provider_home')
    else:
        form = GuideForm()
    return render(request, 'guide_add.html', {'form': form})