from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from core.api.v1.rooms.serializers import (
    ReadRoomRecordSerializer,
    RoomRecordSerializer,
    RoomSerializer,
    StuffRoomRecordSerializer,
)
from core.apps.rooms.models import Room, RoomRecord


class RoomRecordsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = RoomRecord.objects.order_by("-date")
    serializer_class = ReadRoomRecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(room=self.request.user.room)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CreateRoomRecordsViewSet(
    CreateModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = RoomRecord.objects.order_by("-date")
    serializer_class = RoomRecordSerializer
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == "today_created":
            return StuffRoomRecordSerializer
        if self.action == "list":
            return RoomSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == "today_created":
            return super().get_queryset().filter(author=self.request.user)
        if self.action == "list":
            return Room.objects.order_by("-number")
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @action(methods=("GET",), detail=False)
    def today_created(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
