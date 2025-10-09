# home/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/jobs/$", consumers.JobConsumer.as_asgi()),   # -----> ws://.../ws/jobs/
    re_path(r"ws/notify/$", consumers.NotificationConsumer.as_asgi())
]
