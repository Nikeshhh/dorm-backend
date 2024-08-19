from rest_framework.routers import DefaultRouter

from core.api.v1.rooms.views import RoomRecordsViewSet, RoomsViewSet


router = DefaultRouter()
router.register("records", RoomRecordsViewSet, "room_records")
router.register("", RoomsViewSet, "rooms")


urlpatterns = [] + router.urls
