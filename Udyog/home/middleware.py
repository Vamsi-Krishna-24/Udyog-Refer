from django.shortcuts import render

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            role = getattr(user, "role", None)

            # Referrer-only pages
            if request.path.startswith("/referer_home") or request.path.startswith("/my_tracker"):
                if role != "referrer":
                    return render(request, "access_denied.html", {"required_role": "Referrer"})

            # Referee-only pages
            if (
                request.path.startswith("/active_referals")
                or request.path.startswith("/trending")
                or request.path.startswith("/tracker")
            ):
                if role != "referee":
                    return render(request, "access_denied.html", {"required_role": "Referee"})

        return self.get_response(request)
