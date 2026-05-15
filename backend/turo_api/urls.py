from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet, ExpertisePostViewSet, SessionSlotViewSet, TutorAvailabilityViewSet,
    BookingViewSet, MessageViewSet, PaymentViewSet, AdminTierRequestsView, AdminTierDecisionView,
    ConversationListView
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'posts', ExpertisePostViewSet)
router.register(r'session-slots', SessionSlotViewSet)
router.register(r'availability', TutorAvailabilityViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('admin/tier-requests/', AdminTierRequestsView.as_view()),
    path('admin/tier-requests/<int:profile_id>/', AdminTierDecisionView.as_view()),
    path('conversations/', ConversationListView.as_view()),
    path('', include(router.urls)),
]
