from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, SubscriberViewSet, BeneficiaryViewSet, ServiceDurationViewSet, ZoneCoverViewSet, AgeRangeViewSet, PricingViewSet, ContractViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'user-answers', UserAnswerViewSet)
router.register(r'subscribers', SubscriberViewSet)
router.register(r'beneficiaries', BeneficiaryViewSet)
router.register(r'service-durations', ServiceDurationViewSet)
router.register(r'zone-covers', ZoneCoverViewSet)
router.register(r'age-ranges', AgeRangeViewSet)
router.register(r'pricings', PricingViewSet)
router.register(r'contracts', ContractViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
