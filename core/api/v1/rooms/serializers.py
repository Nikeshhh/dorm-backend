from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    IntegerField,
    CharField,
)
from core.apps.rooms.models import Room, RoomRecord
from core.apps.users.models import CustomUser


class RecordAuthorSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("surname", "name", "second_name")


class ReadRoomRecordSerializer(ModelSerializer):
    author = RecordAuthorSerializer()

    class Meta:
        model = RoomRecord
        fields = (
            "pk",
            "date",
            "grade",
            "comments",
            "author",
        )


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "number",
        )


class StuffRoomRecordSerializer(ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = RoomRecord
        fields = (
            "pk",
            "grade",
            "comments",
            "room",
        )


class RoomRecordSerializer(Serializer):
    grade = IntegerField()
    comments = CharField(required=False)
    room_pk = IntegerField(required=False)
