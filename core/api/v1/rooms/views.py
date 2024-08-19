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

from drf_spectacular.utils import extend_schema

from django.utils import timezone


class RoomRecordsViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = RoomRecord.objects.order_by("-date")
    serializer_class = ReadRoomRecordSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update"):
            return [IsAdminUser()]
        # Это работает
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "today_created":
            return StuffRoomRecordSerializer
        elif self.action in ("create", "update", "partial_update"):
            return RoomRecordSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action in ("list", "retreive", "my_last_room_record"):
            return self.queryset.filter(room=self.request.user.room)
        elif self.action == "today_created":
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
        return super().get_queryset()

    @extend_schema(tags=["Rooms"])
    def list(self, request, *args, **kwargs):
        """Получить список всех записей комнаты пользователя."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Rooms"])
    def retrieve(self, request, *args, **kwargs):
        """
        Получить запись по ID.

        Получить можно только запись, принадлежащую к комнате пользователя.
        Иначе выбрасывает 404.

        :param id: ID записи.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=["Rooms"])
    @action(methods=("GET",), detail=False, url_path="last")
    def my_last_room_record(self, request, *args, **kwargs):
        """Получить последнюю запись в книге комнаты пользователя."""
        last_record = self.get_queryset().first()

        serializer = self.get_serializer(last_record)

        return Response(serializer.data, HTTP_200_OK)

    queryset = RoomRecord.objects.order_by("-date")
    serializer_class = RoomRecordSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(tags=["Rooms"])
    def create(self, request, *args, **kwargs):
        """Создать запись в книге комнаты."""
        return super().create(request, *args, **kwargs)

    @extend_schema(tags=["Rooms"])
    def update(self, request, *args, **kwargs):
        """Обновить запись в книге комнаты."""
        return super().update(request, *args, **kwargs)

    @extend_schema(tags=["Rooms"])
    def partial_update(self, request, *args, **kwargs):
        """Обновить частично запись в книге комнаты."""
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(tags=["Rooms"])
    @action(methods=("GET",), detail=False, url_path="today/created")
    def today_created(self, request, *args, **kwargs):
        """Получить записи, созданные сегодня."""
        return super().list(request, *args, **kwargs)


class RoomsViewSet(ListModelMixin, GenericViewSet):
    queryset = Room.objects.order_by("-number")
    serializer_class = RoomSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(tags=["Rooms"])
    def list(self, request, *args, **kwargs):
        """Получить список комнат."""
        return super().list(request, *args, **kwargs)
