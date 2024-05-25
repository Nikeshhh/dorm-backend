from datetime import timedelta
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from core.api.v1.rooms.serializers import (
    ReadRoomRecordSerializer,
    RoomRecordSerializer,
    RoomSerializer,
    StuffRoomRecordSerializer,
)
from core.apps.rooms.models import Room, RoomRecord

from django.utils import timezone


class RoomRecordsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = RoomRecord.objects.order_by("-date")
    serializer_class = ReadRoomRecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(room=self.request.user.room)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=("GET",), detail=False)
    def my_last_room_record(self, request, *args, **kwargs):
        last_record = self.get_queryset().first()

        serializer = self.get_serializer(last_record)

        return Response(serializer.data, HTTP_200_OK)


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
            today_date = timezone.now().date()
            return (
                super()
                .get_queryset()
                .filter(
                    author=self.request.user,
                    date__gte=today_date,
                    date__lt=today_date + timedelta(days=1),
                )
            )
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
