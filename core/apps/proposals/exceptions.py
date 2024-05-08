from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST


class ProposalsBaseAPIException(APIException): ...


class ProposalAccessException(ProposalsBaseAPIException):
    status_code = HTTP_403_FORBIDDEN


class ProposalStatusException(ProposalsBaseAPIException):
    status_code = HTTP_400_BAD_REQUEST
