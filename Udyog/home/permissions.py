from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsReferrerOnCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated and request.user.role == "referrer"
        return True

    

class IsReferrer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "referrer"

class IsReferee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "referee"