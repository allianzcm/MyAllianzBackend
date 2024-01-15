from django.utils.translation import gettext_lazy as _
from App.utils.views import CoreBaseModelViewSet
from gifts.filters import GiftRequestFilter
from rest_framework.response import Response
from . serializers import *

class GiftView(CoreBaseModelViewSet):
    serializer_class = GiftSerializer

class GiftRequestView(CoreBaseModelViewSet):
    serializer_class = GiftRequestSerializer
    filter_class= GiftRequestFilter
    filterset_fields = ['user','validated_by','status']
    
    # def create(self, request, *args, **kwargs):
    #     user = self.request.user
    #     return Response(data={'stars':user.stars})
        # return super().create(request, *args, **kwargs)
# @api_view(['GET'])
# def mailing(request):
#     email = request.GET.get('email')
#     print(email)
#     code = random.randint(2365, 7899)
#     msg = f'we send your a verification code to  {email}  check you E-Mail for the code'
#     send(msg=msg)
#     # send_mail(subject=subjects, message=message, from_email="9e206c1e378ce9", recipient_list=recipients)
#     return Response({'msg':msg})
