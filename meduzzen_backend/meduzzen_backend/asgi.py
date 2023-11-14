"""
ASGI config for meduzzen_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

from apps.notifications.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meduzzen_backend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
