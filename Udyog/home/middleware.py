from django.shortcuts import render

class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            role = getattr(user, "role", None)

            # --- Referrer-only pages ---
            if (
                request.path.startswith("/referer_home")
                or request.path.startswith("/my_tracker")
            ):
                if role != "referrer":
                    print(f"[ROLE MIDDLEWARE] Access denied → Referrer-only page | Role={role}")
                    return render(request, "access_denied.html", {"required_role": "Referrer"})
            
            # --- Referee-only pages ---
            elif (
                request.path.startswith("/active_referals")
                or request.path.startswith("/trending")
                or (request.path == "/tracker")  # exact match only
            ):
                if role != "referee":
                    print(f"[ROLE MIDDLEWARE] Access denied → Referee-only page | Role={role}")
                    return render(request, "access_denied.html", {"required_role": "Referee"})

        response = self.get_response(request)
        return response
