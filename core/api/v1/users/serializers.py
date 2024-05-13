from rest_framework.serializers import (
    Serializer,
    CharField,
    SerializerMethodField,
    IntegerField,
)


class UserSerializer(Serializer):
    username = CharField()
    surname = CharField()
    name = CharField()
    second_name = CharField()


class ResidentSerializer(Serializer):
    pk = IntegerField()
    surname = CharField()
    name = CharField()
    room_number = SerializerMethodField()

    def get_room_number(self, instance):
        return instance.room.number
