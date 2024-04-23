from rest_framework.routers import DefaultRouter

from core.api.v1.rooms.views import RoomRecordsViewSet, CreateRoomRecordsViewSet


router = DefaultRouter()
router.register('room_records', RoomRecordsViewSet, 'room_records')
router.register('create_room_records', CreateRoomRecordsViewSet, 'create_room_records')


urlpatterns = [

] + router.urls
