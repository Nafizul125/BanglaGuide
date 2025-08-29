import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


def _cache_key(city: str, date_str: str) -> str:
    return f"weather:{city.lower()}:{date_str}"


def _in_5day_window(date_str: str) -> bool:
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return False
    today = datetime.utcnow().date()
    return today <= target <= (today + timedelta(days=5))


def forecast_for(city: Optional[str], date_str: str) -> Dict[str, Any]:
    city = (city or getattr(settings, "DEFAULT_CITY", "Dhaka")).strip()
    if not city or not date_str:
        return {"ok": False, "reason": "bad_request"}

    if not _in_5day_window(date_str):
        return {"ok": False, "reason": "outside_window"}

    key = _cache_key(city, date_str)
    cached = cache.get(key)
    if cached:
        return cached

    api_key = getattr(settings, "WEATHER_API_KEY", "")
    if not api_key:
        logger.warning("WEATHER_API_KEY not configured")
        return {"ok": False, "reason": "api_error"}

    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {"q": city, "appid": api_key, "units": "metric"}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        preferred_hours = {"09:00:00", "12:00:00", "15:00:00"}
        candidates = []
        for item in data.get("list", []):
            dt_txt = item.get("dt_txt")
            if not dt_txt:
                continue
            dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
            if dt.date() == target_date:
                candidates.append(item)

        if not candidates:
            cache.set(key, {"ok": False, "reason": "no_data"}, 1800)
            return {"ok": False, "reason": "no_data"}

        preferred = [c for c in candidates if c["dt_txt"].split(" ")[1] in preferred_hours]
        chosen = preferred[0] if preferred else candidates[0]

        result = {
            "ok": True,
            "temp": int(round(chosen["main"]["temp"])),
            "condition": chosen["weather"][0]["main"],
        }
        cache.set(key, result, 1800)
        return result
    except requests.RequestException:
        logger.exception("Weather API error")
        return {"ok": False, "reason": "api_error"}