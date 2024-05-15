from rest_framework.routers import DefaultRouter

from core.api.v1.duties.views import (
    DutyRecordsViewSet,
    SwapDutiesViewSet,
    SwapPeopleViewSet,
    SwapRequestsViewSet,
)

router = DefaultRouter()

router.register("records", DutyRecordsViewSet, basename="duty-records")
router.register("swap-duties", SwapDutiesViewSet, basename="duty-swaps")
router.register("swap-people", SwapPeopleViewSet, basename="people-swaps")
router.register("swap-requests", SwapRequestsViewSet, basename="requests-swaps")

urlpatterns = [] + router.urls
