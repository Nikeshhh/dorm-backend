from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import login, authenticate

from core.api.v1.authentication.serializers import LoginSerializer


class AuthenticationViewSet(GenericViewSet):
    serializer_class = LoginSerializer

    @action(methods=('POST', ), detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed()
        
        login(request, user)

        return Response(
            {'data': 'Успешная авторизация'},
            HTTP_200_OK
        )
    
    @action(methods=('GET', ), detail=False)
    def get_user(self, request, *args, **kwargs):
        return Response(
            {'user': str(request.user)}
        )