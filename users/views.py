from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.db.models import Q as orWhere
from django.shortcuts import get_object_or_404 
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser
from knox.models import AuthToken
from knox.views import LoginView, LogoutView, LogoutAllView
from knox.auth import TokenAuthentication
from App.utils.permissions import IsUserActiveUser
from .serializers import *
from . models import ValidationCodes
import random

User = get_user_model()

# register new user 
class SignUpUserView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # return Response(data=request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if request.data['avatar']:
            user.avatar = request.data['avatar']
            user.save()
        if request.data['lang']:
            user.language = request.data['lang']
            user.save()
        return Response({
            "users": UserSerializer(user, context=self.get_serializer_context()).data[0]
        })

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
        data = {
            'user': serializer_data,
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
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated , IsAdminUser ]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        data = request.GET
        users = self.get_queryset().filter(is_active=data.get(
            'status', False), deleted_at=data.get('deleted', None))

        if data['s'] is not None or data['s'] is not "":
            users.filter(
                orWhere(first_name__icontains=data['s']) |
                orWhere(last_name__icontains=data['s']) |
                orWhere(phone__icontains=data['s']) |
                orWhere(email=data['s'])
            )
        if (data['dob'] is not None ):
            users.filter(dob=data['dob'])
        if (data['gender'] is not None ):
            users.filter(gender=data['gender'])
        serialized_data = self.get_serializer(users)
        
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

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

