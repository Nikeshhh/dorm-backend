from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


class DutiesBaseAPIException(APIException): ...


class DutyIsLockedException(DutiesBaseAPIException):
    status_code = HTTP_403_FORBIDDEN


class DutySwapException(DutiesBaseAPIException):
    status_code = HTTP_400_BAD_REQUEST


class SwapRequestStatusException(DutiesBaseAPIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Статус заявки не позволяет провести это действие"
