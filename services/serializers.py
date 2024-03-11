from django.contrib.auth import get_user_model
from rest_framework import serializers
# The line `model = Product` in the `ProductSerializer` class is specifying the model class that the serializer should be based on. In this case, the `ProductSerializer` is designed to serialize instances of the `Product` model. This allows the serializer to automatically generate the fields based on the model definition, making it easier to work with data serialization and deserialization in Django REST framework.
from .models import (AgeRange, Beneficiary, Contract, Pricing, Product, Question, ServiceDuration,
    Subscriber, UserAnswer, ZoneCover)

USER = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
        
class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'

class ServiceDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDuration
        fields = '__all__'

class ZoneCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneCover
        fields = '__all__'

class AgeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeRange
        fields = '__all__'

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
