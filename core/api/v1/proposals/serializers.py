from rest_framework.serializers import (
    Serializer,
    CharField,
    IntegerField,
    DateTimeField,
)

from core.api.v1.duties.serializers import ResidentSerializer
from core.apps.proposals.models import RepairProposal


class ExecutorSerializer(Serializer):
    pk = IntegerField()
    surname = CharField()
    name = CharField()
    second_name = CharField()


class RepairProposalSerializer(Serializer):
    pk = IntegerField(required=False)
    author = ResidentSerializer(required=False)
    description = CharField()
    status = IntegerField(required=False)
    created_at = DateTimeField(required=False)
    executor = ExecutorSerializer(required=False)

    def create(self, validated_data):
        description = validated_data.get("description")

        instance = RepairProposal.objects.create(
            description=description, author=self.context.get("request").user
        )

        return instance
