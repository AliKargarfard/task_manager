from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    اجازه دسترسی فقط برای مالک شیء
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    
class IsCategoryOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user    