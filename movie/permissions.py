from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrSafeMethodsPermission(BasePermission):
    """
    Non staff users can only use SAFE_METHODS
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class IsOwnerOrReadAndCreateOnly(BasePermission):
    """
    Creates a new permission for the ProductViewSet class, if the user is not a product owner or a superuser, can only
    use SAFE_METHODS
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.user == request.user:
            return True

        return request.method in (*SAFE_METHODS, 'POST')
