from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.apps.laundry.models import LaundryRecord


class LaundrySerializer(ModelSerializer):
    is_owned = SerializerMethodField()
    class Meta:
        model = LaundryRecord
        fields = (
            'pk',
            'record_date',
            'time_start',
            'time_end',
            'is_available',
            'is_owned'
        )

    def get_is_owned(self, obj):
        return self.context.get('request').user == obj.owner