"""Reusable role-based DRF permissions.

The custom User model exposes `role` (``mijoz`` / ``usta``) and a helper
``is_master`` property. These permissions key off those.
"""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsClient(BasePermission):
    """Only clients (mijoz) may perform the action."""

    message = "Faqat mijozlar uchun."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_client)


class IsMaster(BasePermission):
    """Only masters (usta) may perform the action."""

    message = "Faqat ustalar uchun."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_master)


class IsOwnerOrReadOnly(BasePermission):
    """Write access only to the object owner; reads open to authenticated users.

    Looks for an owner via common attribute names.
    """

    owner_fields = ("user", "owner", "client", "author", "recipient")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        for field in self.owner_fields:
            if hasattr(obj, field):
                return getattr(obj, field) == request.user
        return False
