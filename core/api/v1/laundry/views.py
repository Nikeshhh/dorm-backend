from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.utils import timezone

from core.api.v1.laundry.serializers import LaundrySerializer
from core.apps.laundry.models import LaundryRecord


class LaundryRecordViewSet(ListModelMixin, GenericViewSet):
    queryset = LaundryRecord.objects.all()
    serializer_class = LaundrySerializer
    permission_classes = (IsAuthenticated, )

    def filter_queryset(self, queryset):
        if self.action == 'today_records_list':
            today = timezone.now().date()
            return queryset.filter(record_date=today)
        return queryset
    
    @action(methods=('GET', ), detail=False)
    def today_records_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=('POST',), detail=True)
    def take_record(self, request, *args, **kwargs):
        record = self.get_object()

        if not record.is_available:
            raise PermissionDenied('Запись уже занята')
        
        record.owner = request.user
        record.save()

        return Response({'data': 'Успешная запись'})