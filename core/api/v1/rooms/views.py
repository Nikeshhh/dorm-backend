from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.api.v1.rooms.serializers import ReadRoomRecordSerializer, RoomRecordSerializer
from core.apps.rooms.models import RoomRecord


class RoomRecordsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = RoomRecord.objects.order_by('-date')
    serializer_class = ReadRoomRecordSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(room=self.request.user.dorm.room)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class CreateRoomRecordsViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = RoomRecord.objects.all()
    serializer_class = RoomRecordSerializer
    permission_classes = (IsAdminUser, )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)