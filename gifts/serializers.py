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
    class Meta:
        model = GiftRequest
        fields = '__all__'

    def validate(self, values):
        print(values['gift'].id)
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
