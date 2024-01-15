from django.urls import path
from rest_framework.routers import DefaultRouter
from . views import *

routers = DefaultRouter()

routers.register('gifts', GiftView, 'gifts')
routers.register('gifts_request', GiftRequestView, '/gifts_request')

urlpatterns = [
    # path(route='mail', view=mailing, name='send_mail'),
    # path(route='gifts_request', view=GiftListView.as_view(), name='gifts_request'),
]

urlpatterns += routers.urls
