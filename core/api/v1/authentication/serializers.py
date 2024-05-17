from rest_framework.serializers import Serializer, CharField


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField()
