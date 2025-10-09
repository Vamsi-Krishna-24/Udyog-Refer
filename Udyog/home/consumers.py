# home/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class JobConsumer(AsyncJsonWebsocketConsumer):
    group = "jobs"  # -----> all clients join same broadcast group

    async def connect(self):
        await self.channel_layer.group_add(self.group, self.channel_name)   # join
        await self.accept()
        await self.send_json({"type": "hello", "msg": "connected"})         # optional handshake

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # -----> handle client messages (optional)
        if content.get("type") == "ping":
            await self.send_json({"type": "pong"})

    # -----> server -> client broadcast handler
    async def job_event(self, event):
        # event = {"type": "job.event", "payload": {...}}
        await self.send_json({"type": "job", **event["payload"]})



User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # parse token from querystring: ws://...?token=XYZ
        token = self.scope["query_string"].decode().split("token=")[-1]
        try:
            user_id = AccessToken(token)["user_id"]
            self.user = await User.objects.aget(id=user_id)
        except Exception:
            self.user = AnonymousUser()

        if self.user.is_anonymous:
            await self.close()
        else:
            # subscribe to that user's group
            self.group_name = f"referrer_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send(text_data=json.dumps({"status": "connected"}))

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # handler that receives events from backend
    async def seeker_request_created(self, event):
        await self.send(text_data=json.dumps(event["data"]))
