from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from . models import *
from users.serializers import UserSerializer


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'


class GiftRequestSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # gift = GiftSerializer()
    class Meta:
        model = GiftRequest
        fields = '__all__'

    def validate(self, attrs):
        # if not attrs['user']:
        #     raise ValidationError(detail={'msg': _('invalid user credentials')} , code=HTTP_401_UNAUTHORIZED)
        return attrs
