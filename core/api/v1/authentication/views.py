from django.http import HttpRequest
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema

import logging

from core.api.v1.authentication.serializers import LoginSerializer


logger = logging.getLogger(__name__)


class AuthenticationViewSet(GenericViewSet):
    serializer_class = LoginSerializer

    @extend_schema(tags=["Authentication"])
    @action(methods=("POST",), detail=False)
    def login(self, request: HttpRequest, *args, **kwargs):
        """Аутентифицирует пользователя."""
        serializer = self.get_serializer(request.data)

        user = authenticate(**serializer.data)

        if user is None:
            logger.debug(
                f"Безуспешная попытка авторизации от {request.META.get('REMOTE_ADDR')}"
            )
            raise AuthenticationFailed

        login(request, user)

        return Response({"data": "Успешная авторизация"}, HTTP_200_OK)

    @extend_schema(tags=["Authentication"])
    @action(methods=("POST",), detail=False)
    def logout(self, request, *args, **kwargs):
        """Удаляет authentication credentials из текущего запроса."""
        logout(request)
        return Response({"data": "Успешный выход из аккаунта"}, HTTP_200_OK)

    @extend_schema(tags=["Authentication"])
    @action(methods=("GET",), url_path="is-authenticated", detail=False)
    def is_authenticated(self, request, *args, **kwargs):
        """Возвращает true, если пользователь авторизован, иначе false."""
        return Response(
            {"is_authenticated": not isinstance(request.user, AnonymousUser)}
        )
