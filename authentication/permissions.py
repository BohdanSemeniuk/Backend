from rest_framework.permissions import BasePermission


class IsUnauthenticated(BasePermission):
    """
    Creates a new permission for the RegisterAPIView and LoginAPIView, only unauthenticated users can register and login
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is False
