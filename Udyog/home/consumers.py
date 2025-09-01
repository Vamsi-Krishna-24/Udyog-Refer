# home/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

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
