from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_200_OK
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone

from drf_spectacular.utils import extend_schema

from core.api.v1.laundry.serializers import LaundrySerializer
from core.apps.laundry.exceprtions import RecordStateException
from core.apps.laundry.models import LaundryRecord
from core.apps.laundry.services import create_laundry_records_for_today


class LaundryRecordViewSet(ListModelMixin, GenericViewSet):
    queryset = LaundryRecord.objects.order_by("time_start")
    serializer_class = LaundrySerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        if self.action == "today_records_list":
            today = timezone.now().date()
            return queryset.filter(record_date=today)
        return queryset

    @extend_schema(tags=["Laundry"])
    @action(methods=("GET",), detail=False)
    def today_records_list(self, request, *args, **kwargs):
        """
        Получить список записей на сегодняшний день.
        При отсуствии записей, происходит создание новых на сегодня.
        """
        if not self.filter_queryset(self.get_queryset()):
            create_laundry_records_for_today()
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Laundry"])
    @action(methods=("POST",), detail=True)
    def take_record(self, request, *args, **kwargs):
        """
        Зарезервировать запись.

        :param id: ID записи.
        :raises RecordStateException: Если запись уже занята.
        """
        record = self.get_object()

        if not record.is_available:
            raise RecordStateException("Запись уже занята")

        record.owner = request.user
        record.save()

        return Response({"detail": "Успешная запись"})

    @extend_schema(tags=["Laundry"])
    @action(methods=("POST",), detail=True)
    def free_record(self, request, *args, **kwargs):
        """
        Освободить запись.

        :param id: ID записи.
        :raises RecordStateException: Если запись уже свободна.
        :raises PermissionDenied: Если запись не принадлежит текущему пользователю.
        """
        record = self.get_object()

        if record.is_available:
            raise RecordStateException("Запись уже свободна")

        if not record.owner == request.user:
            raise PermissionDenied("Запись вам не принадлежит")

        record.owner = None
        record.save()

        return Response({"detail": "Запись успешно освобождена"})

    @extend_schema(tags=["Laundry"])
    @action(methods=("GET",), detail=False)
    def my_records_today(self, request, *args, **kwargs):
        """Получить список сегодняшних записей, зарезервированных текущим пользователем."""
        today = timezone.now().date()
        user = request.user
        records = self.get_queryset().filter(record_date=today).filter(owner=user)

        serializer = self.get_serializer(records, many=True)

        return Response(serializer.data, HTTP_200_OK)

    @extend_schema(tags=["Laundry"])
    @action(methods=("GET",), detail=False)
    def today_records_stats(self, request, *args, **kwargs):
        """
        Получить статистику записей на сегодняшний день.
        Возвращает строку, которая сообщает количество свободных записей,
        или сообщение об отсуствии свободных записей.
        """
        today = timezone.now().date()
        records_count = (
            self.get_queryset().filter(owner=None, record_date=today).count()
        )
        if records_count > 0:
            message = f"Свободно {records_count} записей"
        else:
            message = "На сегодня нет свободных записей"

        return Response({"message": message}, HTTP_200_OK)

    @extend_schema(tags=["Laundry"])
    def list(self, request, *args, **kwargs):
        """Получить список всех записей."""
        return super().list(request, *args, **kwargs)
