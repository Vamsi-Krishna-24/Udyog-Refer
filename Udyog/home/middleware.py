# Udyog/home/middleware.py
from django.shortcuts import redirect

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        path = request.path

        # Skip middleware checks for APIs and unauthenticated users
        if path.startswith("/api/") or not user or not user.is_authenticated:
            return self.get_response(request)

        role = getattr(user, "role", None)

        # Allow referrers
        if path.startswith("/referer_home") and role != "referrer":
            return redirect("/access_denied")

        # Allow referees
        if path.startswith("/active_referals") and role != "referee":
            return redirect("/access_denied")

        return self.get_response(request)
