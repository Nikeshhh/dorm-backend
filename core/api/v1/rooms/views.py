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
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from drf_spectacular.utils import extend_schema

from core.api.v1.rooms.serializers import (
    ReadRoomRecordSerializer,
    RoomRecordSerializer,
    RoomSerializer,
    StuffRoomRecordSerializer,
)
from core.apps.rooms.models import Room, RoomRecord
from core.apps.rooms.services import RoomRecordsService


class RoomRecordsViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = RoomRecord.objects.order_by("-date")
    serializer_class = ReadRoomRecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update"):
            return [IsAdminUser()]
        # Это работает
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "today_created":
            return StuffRoomRecordSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        room_records_service = RoomRecordsService(current_user=self.request.user)
        if self.action in ("list", "retreive", "my_last_room_record"):
            return room_records_service.list_user_room_records()
        elif self.action == "today_created":
            return room_records_service.list_created_by_user_today()
        return super().get_queryset()

    @extend_schema(tags=["Rooms"])
    def list(self, request, *args, **kwargs):
        """Получить список всех записей комнаты пользователя."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Rooms"])
    def retrieve(self, request, pk, *args, **kwargs):
        """
        Получить запись по ID.

        Получить можно только запись, принадлежащую к комнате пользователя.
        Иначе выбрасывает 404.

        :param id: ID записи.
        """
        room_records_service = RoomRecordsService(current_user=self.request.user)
        room_record = room_records_service.get_by_id(id=pk)

        serializer = self.get_serializer(room_record)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @extend_schema(tags=["Rooms"])
    @action(methods=("GET",), detail=False, url_path="last")
    def my_last_room_record(self, request, *args, **kwargs):
        """Получить последнюю запись в книге комнаты пользователя."""
        room_records_service = RoomRecordsService(current_user=self.request.user)

        last_record = room_records_service.get_user_last_record()

        serializer = self.get_serializer(last_record)
        return Response(serializer.data, HTTP_200_OK)

    @extend_schema(tags=["Rooms"])
    def create(self, request, *args, **kwargs):
        """Создать запись в книге комнаты."""
        serializer = RoomRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_record = RoomRecordsService.create(
            room_id=serializer.data.get("room_pk"),
            grade=serializer.data.get("grade"),
            comments=serializer.data.get("comments"),
            author=request.user,
        )

        serializer = ReadRoomRecordSerializer(new_record)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @extend_schema(tags=["Rooms"])
    def update(self, request, pk, *args, **kwargs):
        """Обновить запись в книге комнаты."""
        serializer = RoomRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room_records_service = RoomRecordsService(current_user=request.user)
        current_record = room_records_service.get_by_id(id=pk)

        room_records_service = RoomRecordsService(
            current_user=self.request.user, room_record=current_record
        )

        updated_record = room_records_service.update(
            grade=serializer.data.get("grade"),
            comments=serializer.data.get("comments"),
        )

        serializer = ReadRoomRecordSerializer(updated_record)
        return Response(serializer.data, status=HTTP_200_OK)

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
