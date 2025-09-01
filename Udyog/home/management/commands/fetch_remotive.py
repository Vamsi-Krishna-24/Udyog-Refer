# home/management/commands/fetch_remotive.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# ... inside loop, after obj saved:
channel_layer = get_channel_layer()
payload = {
    "id": obj.id,
    "company": obj.company,
    "position": obj.position,
    "location": obj.location,
    "url": obj.url,
    "salary": obj.salary,
    "published_at": obj.published_at.isoformat() if obj.published_at else None,
    "description": obj.description[:180],  # keep it light
}

# -----> only broadcast when created (or when fields changed)
if is_created:
    async_to_sync(channel_layer.group_send)(
        "jobs",
        {"type": "job.event", "payload": payload}   # maps to job_event() in consumer
    )
