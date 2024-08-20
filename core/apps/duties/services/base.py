from abc import ABC, abstractmethod

from core.apps.duties.models import SwapDutiesRequest, SwapPeopleRequest
from core.apps.users.models import CustomUser as UserModel


type SwapRequest = SwapPeopleRequest | SwapDutiesRequest


class BaseSwapRequestService(ABC):
    """
    Базовый класс для сервисов обмена.
    """

    def create(self, *args, **kwargs) -> SwapRequest:
        """Создать заявку"""
        ...

    @abstractmethod
    def accept(self, user: UserModel) -> None:
        """Принять заявку"""
        ...

    @abstractmethod
    def decline(self, user: UserModel) -> None:
        """Отклонить заявку"""
        ...

    @abstractmethod
    def cancel(self, user: UserModel) -> None:
        """Отменить заявку"""
        ...
