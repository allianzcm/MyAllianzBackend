from . models import Gift , GiftRequest
import django_filters

class GiftRequestFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model=GiftRequest
        fields = ['user','gift','validated_by','status']