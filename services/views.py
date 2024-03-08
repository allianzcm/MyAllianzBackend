from rest_framework import viewsets
from .models import Product, Subscriber, Beneficiary, ServiceDuration, ZoneCover, AgeRange, Pricing, Contract
from .serializers import ProductSerializer, SubscriberSerializer, BeneficiarySerializer, ServiceDurationSerializer, ZoneCoverSerializer, AgeRangeSerializer, PricingSerializer, ContractSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer

class ServiceDurationViewSet(viewsets.ModelViewSet):
    queryset = ServiceDuration.objects.all()
    serializer_class = ServiceDurationSerializer

class ZoneCoverViewSet(viewsets.ModelViewSet):
    queryset = ZoneCover.objects.all()
    serializer_class = ZoneCoverSerializer

class AgeRangeViewSet(viewsets.ModelViewSet):
    queryset = AgeRange.objects.all()
    serializer_class = AgeRangeSerializer

class PricingViewSet(viewsets.ModelViewSet):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
