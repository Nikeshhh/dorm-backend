from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_403_FORBIDDEN


class BaseUserAPIException(APIException): ...


class RoleViolationException(BaseUserAPIException):
    status_code = HTTP_403_FORBIDDEN
    default_detail = "Ваши роли не позволяют совершить это действие"
