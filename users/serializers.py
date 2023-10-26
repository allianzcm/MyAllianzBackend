from __future__ import annotations
from django.contrib.auth import get_user_model
from django.db.models import Q as OrWhere
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from django.db.models import fields
from rest_framework import serializers
from . models import (UserSettings , ValidationCodes)
from django_countries.serializer_fields import CountryField

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password' ,'groups' ,'user_permissions')
        
        
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
            username = data['username'],
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
            'msg' : _('miss match username or email and password verify. your credentials and try again.')
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
    
    