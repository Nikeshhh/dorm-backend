from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.authentication import SessionAuthentication

from drf_spectacular.utils import extend_schema

from core.api.v1.users.serializers import ResidentSerializer, UserSerializer
from core.apps.users.models import CustomUser
from core.apps.users.services import UserService


class UsersViewSet(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list_residents":
            return ResidentSerializer
        return super().get_serializer_class()

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
        residents_list = (
            UserService.get_all_residents()
            .select_related("room")
            .order_by("room__number")
        )

        serializer = self.get_serializer(residents_list, many=True)

        return Response(serializer.data, HTTP_200_OK)
