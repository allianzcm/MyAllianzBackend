from . models import Gift , GiftRequest
import django_filters

class GiftRequestFilter(django_filters.FilterSet):
    class Meta:
        model=GiftRequest
        fields = ['status']