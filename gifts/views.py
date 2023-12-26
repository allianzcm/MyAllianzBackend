from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT)
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from App.utils.views import CoreBaseModelViewSet
from . serializers import *

class GiftView(CoreBaseModelViewSet):
    serializer_class = GiftSerializer
    model = Gift

class GiftRequestView(ModelViewSet):
    serializer_class = GiftSerializer
    model = GiftRequest

# @api_view(['GET'])
# def mailing(request):
#     email = request.GET.get('email')
#     print(email)
#     code = random.randint(2365, 7899)
#     msg = f'we send your a verification code to  {email}  check you E-Mail for the code'
#     send(msg=msg)
#     # send_mail(subject=subjects, message=message, from_email="9e206c1e378ce9", recipient_list=recipients)
#     return Response({'msg':msg})
