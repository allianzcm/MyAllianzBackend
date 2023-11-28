from rest_framework.permissions import DjangoModelPermissions , BasePermission 
from rest_framework.authentication import get_authorization_header
from knox.models import AuthToken
class AppModelPermission(DjangoModelPermissions):
    
    def has_permission(self, request, view):
        pass
    def has_object_permission(self, request, view, obj):
        pass
    
class IsUserActiveUser(BasePermission):
    def has_permission(self, request, view):
        auth = get_authorization_header(request).split()
        data = {
            'id': request.user.id,
            'token' : auth[1]
        }
        # , token_key=data['token']
        token = AuthToken.objects.filter(user=data['id'] ).exists()
        # raise Exception(token)
        return True