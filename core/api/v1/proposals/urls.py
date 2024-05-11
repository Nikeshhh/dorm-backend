from rest_framework.routers import DefaultRouter

from core.api.v1.proposals.views import RepairProposalsViewSet

router = DefaultRouter()

router.register("repair", RepairProposalsViewSet, basename="repair-proposals")


urlpatterns = [] + router.urls
