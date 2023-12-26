from rest_framework.routers import DefaultRouter
from .views import FAQView

routers = DefaultRouter()
routers.register('faqs', FAQView, 'faqs')

urlpatterns = [

]
urlpatterns += routers.urls
