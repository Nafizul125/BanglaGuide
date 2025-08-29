"""
ASGI config for banglaguide project using Channels.
Ensures Django is configured BEFORE importing chat.routing (which imports models).
"""
import os
import django

# Configure settings early
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banglaguide.settings")
django.setup()

from django.core.asgi import get_asgi_application
from django.conf import settings
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# In development when using Daphne directly we must wrap static files handler
if settings.DEBUG:
    try:
        from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
        django_asgi_app = ASGIStaticFilesHandler(get_asgi_application())
    except Exception:  # Fallback if handler import fails
        django_asgi_app = get_asgi_application()
else:
    django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
})