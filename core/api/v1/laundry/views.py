from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_200_OK
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone

from drf_spectacular.utils import extend_schema

from core.api.v1.laundry.serializers import LaundrySerializer
from core.apps.laundry.models import LaundryRecord
from core.apps.laundry.services import LaundryService, create_laundry_records_for_today


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
    def list(self, request, *args, **kwargs):
        """Получить список всех записей."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Laundry"])
    @action(methods=("GET",), detail=False, url_path="today")
    def today_records_list(self, request, *args, **kwargs):
        """
        Получить список записей на сегодняшний день.

        :side effect: При отсуствии записей, происходит создание новых на сегодня.
        """
        if not self.filter_queryset(self.get_queryset()):
            create_laundry_records_for_today()
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Laundry"])
    @action(methods=("POST",), detail=True, url_path="take")
    def take_record(self, request, pk, *args, **kwargs):
        """
        Зарезервировать запись.

        :param id: ID записи.
        :raises RecordStateException: Если запись уже занята.
        """
        record = LaundryService.get_by_id(id=pk)

        laundry_service = LaundryService(current_user=request.user, record=record)

        laundry_service.take_record()

        return Response({"detail": "Успешная запись"})

    @extend_schema(tags=["Laundry"])
    @action(methods=("POST",), detail=True, url_path="free")
    def free_record(self, request, pk, *args, **kwargs):
        """
        Освободить запись.

        :param id: ID записи.
        :raises RecordStateException: Если запись уже свободна.
        :raises PermissionDenied: Если запись не принадлежит текущему пользователю.
        """
        record = LaundryService.get_by_id(id=pk)

        laundry_service = LaundryService(current_user=request.user, record=record)

        laundry_service.free_record()

        return Response({"detail": "Запись успешно освобождена"})

    @extend_schema(tags=["Laundry"])
    @action(methods=("GET",), detail=False, url_path="today/my")
    def my_records_today(self, request, *args, **kwargs):
        """Получить список сегодняшних записей, зарезервированных текущим пользователем."""
        records = LaundryService.get_users_records_today(request.user)

        serializer = self.get_serializer(records, many=True)

        return Response(serializer.data, HTTP_200_OK)

    @extend_schema(tags=["Laundry"])
    @action(methods=("GET",), detail=False, url_path="today/stats")
    def today_records_stats(self, request, *args, **kwargs):
        """
        Получить статистику записей на сегодняшний день.

        Возвращает строку, которая сообщает количество свободных записей,
        или сообщение об отсуствии свободных записей.
        """
        message = LaundryService.get_today_records_stats()

        return Response({"message": message}, HTTP_200_OK)
