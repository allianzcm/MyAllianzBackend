from App.utils.views import CoreBaseModelViewSet
from faqs.models import FAQ
from faqs.serializers import FAQSerializer


class FAQView(CoreBaseModelViewSet):
    model = FAQ
    serializer_class = FAQSerializer