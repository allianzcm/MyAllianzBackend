from __future__ import annotations
from django.contrib.auth import get_user_model
from django.db.models import Q as OrWhere
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from django.db.models import fields
from rest_framework import serializers
from . models import (UserSettings , ValidationCodes)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password' ,'groups' ,'user_permissions')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups' ,'user_permissions','is_admin','is_staff','is_active','is_superuser','employees')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        user = User.objects.create_user(
            username = data['username'],
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            password = data['password'],
            )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = self.authenticate_user(username=username , password=password)
        if user.is_active:
            return user
        raise serializers.ValidationError({
            'status' : status.HTTP_401_UNAUTHORIZED,
            'msg' : _('UNAUTHORIZED')
        })


    def authenticate_user(self ,username : str ,  password : str):
        user = User.objects.filter(
            OrWhere(username = username ) |
            OrWhere(email = username )
        ).first()
        if user and  user.check_password(password):
            return user
        raise serializers.ValidationError( {
            'status' : status.HTTP_404_NOT_FOUND,
            'msg' : _('Incorrect Credentials Passed.')
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
    
    
    