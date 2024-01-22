from __future__ import annotations
from django.contrib.auth import get_user_model
from django.db.models import Q as OrWhere
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth.models import Group , Permission
from . models import (UserSettings , ValidationCodes)

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model= Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Permission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

    def validate(self, data):
        request_method = self.context['request'].method
        # Check if 'password' is present in the data and if the method is 'put' or 'patch'
        if 'password' in data and request_method == ['PUT', 'PATCH']:
            raise serializers.ValidationError({'password': 'You cannot update the password using this method.'})
        return super(UserSerializer, self).validate(data)


class GetUserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    # user_permissions = PermissionSerializer(many=True)
    class Meta:
        model = User
        exclude = ['password']


    def put_update(self , instance , data):
        try:
            instance.first_name = data['fname'] if (data['fname']) else instance
            instance.last_name = data['lname'] if (data['lname']) else instance
            return instance.save()
        except:
            raise Exception('Failed to update user name')


    def patch_update(self ,instance, data):
        try:
            instance.avatar = data['avatar'] if data['avatar'] else instance
            instance.locale = data['locale'] if data['locale'] else instance
            return instance.save()
        except:
            raise Exception('Failed to update user information')

    def update(self, instance, data):
        method = data['method']
        if method == "PUT":
            return self.put_update(instance=instance , data=data)
        if method == "PATCH":
            return self.patch_update(instance=instance , data=data)
        return instance


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups' ,'user_permissions','is_admin','is_staff','is_active','is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        user = User.objects.create_user(
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            password = data['password'],
            )
        user.gender = data['gender']
        user.phone = data['phone']
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        password = data['password']
        email = data['email']
        user = self.authenticate_user(email=email , password=password)
        if user.is_active:
            return user
        raise serializers.ValidationError({
            'status' : status.HTTP_401_UNAUTHORIZED,
            'msg' : _('UNAUTHORIZED')
        })


    def authenticate_user(self ,email : str ,  password : str):
        user = User.objects.filter(email=email).first()
        if user and  user.check_password(password):
            return user
        raise serializers.ValidationError( {
            'status' : status.HTTP_404_NOT_FOUND,
            'msg' : _('miss match email and password verify. your credentials and try again.')
        })



class UserSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model= UserSettings
        fields = '__all__'

class ValidationCodesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model= ValidationCodes
        fields = '__all__'

    def validate(self , attr):
        if not attr['for'] :
            raise Exception(_("failed to proceed request"))
        return attr

    def create(self, data):
        return self.Meta.model.objects.create(user=data['user'],reset_code=data['code'] , code_for=data['for'])

