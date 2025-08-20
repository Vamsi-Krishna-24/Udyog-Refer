from rest_framework import permissions
class IsReferrerOnCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return getattr(request.user, "role", "").lower() == "referrer"  # -----> your field name
        return True
    