from rest_framework.serializers import (
    Serializer,
    CharField,
    IntegerField,
    DateTimeField,
)

from core.api.v1.duties.serializers import ResidentSerializer


class ExecutorSerializer(Serializer):
    pk = IntegerField()
    surname = CharField()
    name = CharField()
    second_name = CharField()


class RepairProposalSerializer(Serializer):
    pk = IntegerField()
    author = ResidentSerializer()
    description = CharField()
    status = IntegerField()
    created_at = DateTimeField()
    executor = ExecutorSerializer()
