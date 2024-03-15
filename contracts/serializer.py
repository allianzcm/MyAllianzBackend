from rest_framework.serializers import ModelSerializer
from contracts.models import Contract


class ContractSerializer(ModelSerializer):
    class Meta:
        model=Contract
        fields = '__all__'