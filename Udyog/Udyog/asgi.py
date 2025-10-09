# Udyog/asgi.py
# -----> ASGI entrypoint for HTTP + WebSocket
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import home.routing  # -----> your WS routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Udyog.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            home.routing.websocket_urlpatterns
        )
    ),
})


