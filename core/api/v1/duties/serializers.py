from rest_framework.serializers import (
    Serializer,
    CharField,
    SerializerMethodField,
    DateField,
    BooleanField,
    IntegerField,
    DateTimeField,
)


class ResidentSerializer(Serializer):
    pk = IntegerField()
    surname = CharField()
    name = CharField()
    second_name = CharField()
    room = SerializerMethodField()

    def get_room(self, obj):
        return obj.room.number if obj.room else None


class KitchenDutySerializer(Serializer):
    pk = IntegerField()
    date = DateField()
    people = ResidentSerializer(many=True)
    finished = BooleanField()


class SwapDutiesRequestSerializer(Serializer):
    pk = IntegerField()
    first_user = ResidentSerializer()
    second_user = ResidentSerializer()
    first_duty = KitchenDutySerializer(many=False)
    second_duty = KitchenDutySerializer(many=False)

    accepted = BooleanField()
    canceled = BooleanField()
    declined = BooleanField()
    created_at = DateTimeField()


class CreateSwapDutiesRequestSerializer(Serializer):
    initiator_duty_pk = IntegerField()
    to_swap_duty_pk = IntegerField()
    to_swap_resident_pk = IntegerField()


class SwapPeopleRequestSerializer(Serializer):
    pk = IntegerField()
    current_user = ResidentSerializer()
    to_swap = ResidentSerializer()
    duty = KitchenDutySerializer(many=False)

    accepted = BooleanField()
    canceled = BooleanField()
    declined = BooleanField()
    created_at = DateTimeField()


class CreateSwapPeopleRequestSerializer(Serializer):
    to_swap_duty_pk = IntegerField()
    to_swap_user_pk = IntegerField()
