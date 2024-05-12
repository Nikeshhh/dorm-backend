from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    IntegerField,
    CharField,
    ValidationError,
)
from rest_framework.exceptions import NotFound

from core.apps.rooms.models import Room, RoomRecord


class ReadRoomRecordSerializer(ModelSerializer):
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

    def validate(self, attrs):
        if not 2 <= attrs.get("grade") <= 5:
            raise ValidationError("Оценка должна находиться в промежутке от 2 до 5")
        return attrs

    def create(self, validated_data):
        try:
            room = Room.objects.get(pk=validated_data.get("room_pk"))
        except Room.DoesNotExist:
            raise NotFound(f'Комната с pk={validated_data.get('room_pk')} не найдена')
        author = self.context.get("request").user
        instance = RoomRecord.objects.create(
            grade=validated_data.get("grade"),
            comments=validated_data.get("comments"),
            room=room,
            author=author,
        )
        return instance

    def update(self, instance, validated_data):
        instance.grade = validated_data.get("grade")
        instance.comments = validated_data.get("comments")
        instance.save()
        return instance

    def save(self, **kwargs):
        return super().save(**kwargs)
