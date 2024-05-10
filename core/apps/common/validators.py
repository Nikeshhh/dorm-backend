from core.apps.users.exceptions import RoleViolationException
from core.apps.users.models import CustomUser


def user_is_resident(user: CustomUser) -> None:
    if not user.is_resident:
        raise RoleViolationException


def user_is_staff(user: CustomUser) -> None:
    if not user.is_staff:
        raise RoleViolationException


def user_is_worker(user: CustomUser) -> None:
    if not user.is_worker:
        raise RoleViolationException
