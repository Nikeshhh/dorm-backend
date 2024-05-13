from rest_framework.serializers import Serializer, CharField


class UserSerializer(Serializer):
    username = CharField()
    surname = CharField()
    name = CharField()
    second_name = CharField()
