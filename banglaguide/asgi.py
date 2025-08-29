"""
ASGI config for banglaguide project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import routing as project_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banglaguide.settings')

django_app = get_asgi_application()

application = ProtocolTypeRouter({
	'http': django_app,
	'websocket': AuthMiddlewareStack(
		URLRouter(project_routing.websocket_urlpatterns)
	),
})
