from rest_framework import permissions

class AppModelPermission(permissions.DjangoModelPermissions):
    
    def has_permission(self, request, view):
        pass
    def has_object_permission(self, request, view, obj):
        pass