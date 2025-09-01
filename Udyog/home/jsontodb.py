import json
from .models import Jobs 

with open("jobs.json", "r") as f:
    data = json.load(f)

# skip index 0 (metadata)
jobs = data[1:]

for job in jobs:
    company = job.get("company") or "Unknown"
    location = job.get("location") or "Remote"
    description = job.get("description") or "No Description"
    position = job.get("position") or "No Position"
    url = job.get("url") or job.get("apply_url") or ""

    # save to DB
    Jobs.objects.create(
        company=company,
        location=location,
        description=description,
        position=position,
        url=url
    )

print("Jobs pushed to DB successfully 🚀")
