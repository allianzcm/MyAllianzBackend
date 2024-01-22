from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from . models import *
from users.serializers import UserSerializer


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'


class GiftRequestSerializer(serializers.ModelSerializer):
    # gift = GiftSerializer(read_only=True)
    class Meta:
        model = GiftRequest
        fields = '__all__'

    def to_representation(self, instance):
        
        if self.context['request'].method == 'GET':
            representation = super().to_representation(instance)
            representation['user'] = UserSerializer(
                instance.user, read_only=True).data
            representation['gift'] = GiftSerializer(
                instance.gift, read_only=True).data
            return representation
        else:
            return super().to_representation(instance)

    def validate(self, values):
        request = self.context['request']
        if request.method == 'POST':
            user = request.user
            gift = Gift.objects.get(id=values['gift'].id)
            if (user.stars < gift.stars):
                print(gift.stars)
                raise ObjectDoesNotExist(_('not enough  stars to get Gift'))
            user.stars = user.stars - gift.stars
            user.save()
        return super().validate(values)
