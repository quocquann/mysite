from rest_framework.permissions import BasePermission


class CanMarkAsReturned(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("catalog.can_mark_as_returned")
