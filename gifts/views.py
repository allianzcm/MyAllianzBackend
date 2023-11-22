from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT)
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from . serializers import *


def validateUser(request):
    data = request.data
    data['user'] = request.user.id
    return data


class GiftView(ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    serializer_class = GiftSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Gift.objects.all()



class GiftRequestView(ModelViewSet):
    authentication_classes = TokenAuthentication
    serializer_class = GiftSerializer
    permission_classes = [IsAuthenticated]
    queryset = GiftRequest.objects.all()

    def list(self, request, *args, **kwargs):
        data = validateUser(request=request)
        data['user'] = request.user.id
        return super.list(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        data = request.data
        instance = get_object_or_404(self.get_queryset(), id=data['gift'])
        instance.soft_delete()
        return Response(data={'msg': _('resource deleted successfully')}, status=HTTP_204_NO_CONTENT)