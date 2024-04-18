from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class BaseLaundryException(APIException):
    ...


class RecordStateException(BaseLaundryException):
    status_code = HTTP_400_BAD_REQUEST
