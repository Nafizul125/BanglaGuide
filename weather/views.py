from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services import forecast_for


@require_GET
def forecast(request):
    city = request.GET.get("city")
    date_str = request.GET.get("date")
    result = forecast_for(city, date_str)
    return JsonResponse(result, status=200 if result.get("ok") else 400)