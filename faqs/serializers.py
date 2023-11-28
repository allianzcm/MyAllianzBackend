from rest_framework.serializers import ModelSerializer

from faqs.models import FAQ

class FAQSerializer (ModelSerializer):
    class Meta:
        model=FAQ