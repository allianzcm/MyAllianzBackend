from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.utils.translation import gettext_lazy as _
from . models import *
from users.serializers import UserSerializer



class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gifts
    
    def update(self, instance, data):
        instance.name_en = data['name_en'] if data['name_en'] else None
        instance.name_fr = data['name_fr'] if data['name_fr'] else None
        instance.desc_en = data['desc_en'] if data['desc_en'] else None
        instance.desc_fr = data['desc_fr'] if data['desc_fr'] else None
        instance.stars   = data['stars'] if data['stars'] else None
        return instance.save()

class GiftRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    gift = GiftSerializer()
    class Meta:
        model = GiftRequests
    
    def validate(self, attrs):
        # if not attrs['user']:
        #     raise ValidationError(detail={'msg': _('invalid user credentials')} , code=HTTP_401_UNAUTHORIZED)
        return attrs
    