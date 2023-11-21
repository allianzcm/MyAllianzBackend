from django.urls  import path
from rest_framework.routers import DefaultRouter
from . views import *

routers = DefaultRouter()
routers.register('gifts' , GiftView)
routers.register('gifts_request' ,GiftRequestView)

urlpatterns = [
    path(route='mail', view=mailing , name='send_mail'),
]

urlpatterns += routers.urls