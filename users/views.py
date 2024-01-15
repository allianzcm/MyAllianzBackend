import random
import string
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework.decorators import api_view
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Q as OrWhere
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from knox.models import AuthToken
from knox.views import LoginView, LogoutView, LogoutAllView
from knox.auth import TokenAuthentication
from App.utils.permissions import IsUserActiveUser
from App.utils.views import CoreBaseModelViewSet
from .serializers import *
from . models import ValidationCodes
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.views import APIView

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserActiveUser]

    def post(self, request, format=None):
        super().post(request=request, format=format)
        return Response({'msg': _("logout successfully")}, status.HTTP_200_OK)


class LogoutAllDevicesView(LogoutAllView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUserActiveUser]
    def post(self, request, format=None):
        super().post(request=request, format=format)
        return Response({'msg': _("logout from all devices successfully")}, status.HTTP_204_NO_CONTENT)


# return a filtered lists of users
class GetUsersView(generics.ListAPIView):
    serializer_class = GetUserSerializer
    model = serializer_class.Meta.model
    filterset_fields = ['first_name', 'is_admin']

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class UpdateUserProfileView(generics.UpdateAPIView):
    """update user information
    Returns:
        object (User): _description_
    """
    permission_classes = [IsAdminUser | IsUserActiveUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


# generate a user verification code and mail it to a user for verification
class ValidationCodesView(generics.CreateAPIView):
    serializer_class = ValidationCodesSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user
        data['code'] = random.randint(10000000, 99999999)
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
        verification_code = ValidationCodes.objects.filter(
            user=user, reset_code=code).order_by('-created_at')
        diff = timezone.now() - verification_code.first().created_at
        if (verification_code.exists() and diff.total_seconds() <= (300)):
            return Response(data={'msg': "found"}, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': "not found"}, status=status.HTTP_404_NOT_FOUND)


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
    async_task(send_email_async, subject, message, [email])
    return Response({'msg': "mailed send succefulle"})


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def generate_verification_code(self):
        # Generate a random 6-digit code
        return ''.join(random.choices(string.digits, k=6))

    def post(self, request, *args, **kwargs):
        data = request.data
        email_or_phone = data.get('email_or_phone', '')

        try:
            user = User.objects.get(
                OrWhere(email=email_or_phone) | OrWhere(phone=email_or_phone))
        except User.DoesNotExist:
            # Handle the case where the user does not exist
            return Response({'error': 'User not found.'}, status=400)

        # If the user exists, generate and save a verification code
        verification_code = self.generate_verification_code()
        user.verification_code = verification_code
        user.save()

        # Send verification code via email or SMS (phone)
        if '@' in email_or_phone:
            send_mail(
                'Verification Code',
                f'Your verification code is: {verification_code}',
                'from@example.com',
                [email_or_phone],
                fail_silently=False,
            )
        else:
            # Validate and format the phone number
            try:
                parsed_phone_number = phonenumbers.parse(email_or_phone, None)
                formatted_phone_number = phonenumbers.format_number(
                    parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberFormatException:
                return Response({'error': 'Invalid phone number.'}, status=400)

            # Implement  logic for sending SMS goes here
            print(
                f'SMS sent to {formatted_phone_number} with verification code: {verification_code}')

        return Response({'message': 'Verification code sent successfully.'}, status=200)


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the current user
        user = request.user

        # Get the current password and the new password from the request data
        current_password = request.data.get('current_password', None)
        new_password = request.data.get('new_password', None)

        if current_password and new_password:

            # Check if the authentication is successful
            if user is not None and user.check_password(current_password):
                # Update the user's password
                user.set_password(new_password)
                user.save()

                return Response({"detail": "Password successfully updated."}, status=status.HTTP_200_OK)
            else:
                # If authentication fails, return an error response
                return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Current or new password not provided."}, status=status.HTTP_400_BAD_REQUEST)