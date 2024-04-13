from rest_framework.serializers import Serializer, CharField


class LoginSerializer(Serializer):
    login = CharField()
    password = CharField()
