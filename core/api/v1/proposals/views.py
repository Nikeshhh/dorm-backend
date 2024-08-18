from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.authentication import SessionAuthentication

from drf_spectacular.utils import extend_schema

from core.api.v1.proposals.serializers import RepairProposalSerializer
from core.apps.proposals.models import RepairProposal


class RepairProposalsViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = RepairProposal.objects.order_by("-created_at")
    serializer_class = RepairProposalSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        if self.action == "my_proposals":
            return self.queryset.filter(author=self.request.user)
        return super().get_queryset()

    @extend_schema(tags=["RepairProposals"])
    @action(methods=("GET",), detail=False)
    def my_proposals(self, request, *args, **kwargs):
        """Получить заявки текущего пользователя."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["RepairProposals"])
    @action(methods=("POST",), detail=True)
    def accept(self, request, pk, *args, **kwargs):
        """Принять заявку на ремонт."""
        proposal: RepairProposal = self.get_object()
        proposal.accept(request.user)

        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["RepairProposals"])
    @action(methods=("POST",), detail=True)
    def decline(self, request, pk, *args, **kwargs):
        """Отклонить заявку на ремонт."""
        proposal: RepairProposal = self.get_object()
        proposal.decline(request.user)

        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["RepairProposals"])
    @action(methods=("POST",), detail=True)
    def cancel(self, request, pk, *args, **kwargs):
        """Отменить заявку на ремонт."""
        proposal: RepairProposal = self.get_object()
        proposal.cancel(request.user)

        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["RepairProposals"])
    @action(methods=("POST",), detail=True)
    def close(self, request, pk, *args, **kwargs):
        """Закрыть заявку на ремонт."""
        proposal: RepairProposal = self.get_object()
        proposal.close(request.user)

        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["RepairProposals"])
    def list(self, request, *args, **kwargs):
        """Получить список всех заявок на ремонт."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["RepairProposals"])
    def create(self, request, *args, **kwargs):
        """Создать заявку на ремонт."""
        return super().create(request, *args, **kwargs)
