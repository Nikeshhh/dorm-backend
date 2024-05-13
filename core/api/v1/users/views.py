from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.authentication import SessionAuthentication

from core.api.v1.users.serializers import UserSerializer


class UsersViewSet(GenericViewSet):
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=("GET",), detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)

        return Response(serializer.data, HTTP_200_OK)
