# Udyog/asgi.py
# -----> ASGI entrypoint for HTTP + WebSocket
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import home.routing  # -----> your WS routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Udyog.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,                                   # -----> normal HTTP
    "websocket": AuthMiddlewareStack(                          # -----> WS with session auth
        URLRouter(home.routing.websocket_urlpatterns)          # -----> map ws URLs
    ),
})
