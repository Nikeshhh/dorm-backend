from rest_framework.serializers import ModelSerializer

from core.apps.laundry.models import LaundryRecord


class LaundrySerializer(ModelSerializer):
    class Meta:
        model = LaundryRecord
        fields = (
            'pk',
            'record_date',
            'time_start',
            'time_end',
            'is_available'
        )