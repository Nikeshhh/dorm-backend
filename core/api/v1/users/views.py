from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.authentication import SessionAuthentication

from drf_spectacular.utils import extend_schema

from core.api.v1.users.serializers import ResidentSerializer, UserSerializer
from core.apps.users.models import CustomUser


class UsersViewSet(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list_residents":
            return ResidentSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list_residents":
            queryset = (
                queryset.select_related("room")
                .filter(resident=True)
                .order_by("room__number")
            )
        return queryset

    @extend_schema(tags=["Users"])
    @action(methods=("GET",), detail=False)
    def me(self, request, *args, **kwargs):
        """Получить данные текущего пользователя."""
        serializer = self.get_serializer(request.user)

        return Response(serializer.data, HTTP_200_OK)

    @extend_schema(tags=["Users"])
    @action(methods=("GET",), detail=False, url_path="residents")
    def list_residents(self, request, *args, **kwargs):
        """
        Получить список всех жильцов в общежитии.

        Список отсортирован по номеру комнаты.
        """
        serializer = self.get_serializer(self.get_queryset(), many=True)

        return Response(serializer.data, HTTP_200_OK)
