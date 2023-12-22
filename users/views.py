from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework.decorators import api_view
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.db.models import Q as orWhere
from django.shortcuts import get_object_or_404 
from django.contrib.auth.models import Group , Permission
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser
from knox.models import AuthToken
from knox.views import LoginView, LogoutView, LogoutAllView
from knox.auth import TokenAuthentication
from App.utils.permissions import IsUserActiveUser
from App.utils.views import CoreBaseModelViewSet
from .serializers import *
from . models import ValidationCodes
import random
from django_q.tasks import async_task
from django.core.mail import send_mail
User = get_user_model()


class GroupView(CoreBaseModelViewSet):
    serializer_class = GroupSerializer
    model = Group

class PermissionView(CoreBaseModelViewSet):
    serializer_class = PermissionSerializer
    model = Permission



class SignUpUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = request.data

        if data.get('avatar') is not None:
            user.avatar = data.get('avatar')
        if data.get('lang') is not None:
            user.language = data.get('lang')
        if data.get('resident') is not None:
            user.resident = data.get('resident')
        if data.get('country') is not None:
            user.country = data.get('country')
        if data.get('is_admin') == "true":
            user.is_admin = True
        if data.get('groups') is not None:
            user.groups.add(*data.get('groups'))
        user.save()
        return Response(data=UserSerializer(user, context=self.get_serializer_context()).data)

# login user 
class SignInUserView(LoginView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)
        data = self.get_post_response_data(token, instance, user=user)
        return Response(data)

    def get_post_response_data(self, token, instance, user):
        serializer_data = UserSerializer(user).data,
        user = serializer_data[0]
        data = {
            'user': user,
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        return data

# logout user 
class LogOutView(LogoutView):
    permission_classes = [IsUserActiveUser]
    def post(self, request, format=None):
        super().post(request=request, format=format)
        return Response({'msg': _("logout successfully")} , status.HTTP_204_NO_CONTENT)
class LogoutAllDevicesView(LogoutAllView):
    def post(self, request, format=None):
        super().post(request=request, format=format)
        return Response({'msg': _("logout from all devices successfully")} , status.HTTP_204_NO_CONTENT)


# return a filtered lists of users 
class GetUsersView(generics.ListAPIView):
    serializer_class = GetUserSerializer
    model = serializer_class.Meta.model
    filterset_fields = ['first_name', 'is_admin']

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated , IsAdminUser ]
    queryset = User.objects.all()

class UpdateUserProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated , IsAdminUser|IsUserActiveUser ]
    """update user information
    Returns:
        object (User): _description_
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return User.objects.all()
    
    
    def put(self, request, *args, **kwargs):
        data = request.data
        data['method'] = request.METHOD
        try:
            instance = get_object_or_404( self.get_queryset() , id=data['user'])
            serializers_data = self.get_serializer(instance=instance , data=data)
            if(serializers_data.is_valid(raise_exception=True)):
                return Response(data=serializers_data.data)
        except:
            raise Exception("failed to update resource")


    def patch(self, request, *args, **kwargs):
        data = request.data
        data['method'] = request.method
        try:
            instance = get_object_or_404( self.get_queryset() , id=data['user'])
            serializers_data = self.get_serializer(instance=instance , data=data)
            if(serializers_data.is_valid(raise_exception=True)):
                return Response(data=serializers_data.data)
        except:
            raise Exception("failed to update resource")
        
    

# generate a user verification code and mail it to a user for verification 
class ValidationCodesView(generics.CreateAPIView):
    serializer_class = ValidationCodesSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user
        data['code']  = random.randint(10000000, 99999999)
        serialized_data = self.get_serializer(data)
        serialized_data.is_valid(raise_exception=True)
        validation_code = serialized_data.save()
        return Response(data=validation_code.data, status=status.HTTP_201_CREATED)


# verify validation code 
class VerifyValidationCode(generics.RetrieveAPIView):
    serializer_class = ValidationCodesSerializer
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        code = request.Get['code']
        user = request.Get['user']
        verification_code = ValidationCodes.objects.filter( user=user , reset_code = code).order_by('-created_at')
        diff = timezone.now() - verification_code.first().created_at
        if(verification_code.exists() and diff.total_seconds() <= (300)):
            return Response(data={'msg':"found"} , status=status.HTTP_200_OK)
        else:
            return Response(data={'msg':"not found"} , status=status.HTTP_404_NOT_FOUND) 
    
    

class PassWordResetView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            user = User.objects.get(id=data['user_id'])
            verification_code = ValidationCodes.objects.filter(
                user=user).order_by('-created_at').first()
            code_date = verification_code.created_at
            diff = timezone.now() - code_date
            if (diff.total_seconds() <= (300)) and data['new_password'] == data['confirm_password']:
                user.set_password(data['new_password'])
            else:
                return Response({'msg': 'password miss match'})
            return Response(data={'msg': _('password modified successfully')})
        except:
            return Response(data={'msg': _('error while processing the request')})


class RequestPasswordReset(APIView):
    def get(request):
        email = request.GET.get('email')
        user = User.objects.get()
        token = PasswordResetTokenGenerator.make_token(user=user)
        print(token)
        return Response({})

def send_email_async(subject, message, recipient_list):
    # The actual email sending code
    send_mail(subject, message, '9e206c1e378ce9', recipient_list)

@api_view(['GET'])
def mailer(request):
        email = request.GET.get('email')
        subject = "verification Code"
        message = f'you verification code is {random.randint(2035 , 9999)}'
        async_task(send_email_async , subject , message , [email])
        return Response({'msg':"mailed send succefulle"})


