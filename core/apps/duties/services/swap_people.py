from django.db.transaction import atomic

from core.apps.duties.exceptions import DutySwapException, SwapRequestStatusException
from core.apps.duties.models import KitchenDuty, SwapPeopleRequest
from core.apps.duties.services import BaseSwapRequestService, KitchenDutyService
from core.apps.users.exceptions import RoleViolationException
from core.apps.users.models import CustomUser as UserModel


class SwapPeopleService(BaseSwapRequestService):
    """
    Сервис для работы с заявками на замену людей.
    """

    def __init__(
        self, current_user: UserModel, object: SwapPeopleRequest = None
    ) -> None:
        """
        :param current_user: Текущий пользователь при работе сервиса.
        :param object: Объект запроса на замену
        """
        self._object = object
        self._user = current_user

    @classmethod
    def create(
        cls, initiator: UserModel, initiator_duty: KitchenDuty, target: UserModel
    ) -> SwapPeopleRequest:
        """
        Создать новый запрос на замену.

        :returns: SwapPeopleRequest
        :raises RoleViolationException: Если нарушены роли пользователей
        :raises DutySwapException: Если пользователи идентичны
        :raises DutySwapException: Если initiator уже принадлежит к target_duty
        :raises DutySwapException: Если target не принадлежит к target_duty
        """
        if not cls.user_is_resident(initiator) or not cls.user_is_resident(target):
            raise RoleViolationException(
                "Невозможно создать запрос, если один из пользователей не является проживающим"
            )
        if initiator == target:
            raise DutySwapException(
                "Невозможно создать запрос на замену между идентичными пользователями."
            )
        if not initiator_duty.people.contains(initiator):
            raise DutySwapException(
                f"Дежурный {initiator} не принадлежит дежурству {initiator_duty}"
            )
        if initiator_duty.people.contains(target):
            raise DutySwapException(
                f"Дежурный {target} уже принадлежит к дежурству {initiator_duty}"
            )
        return cls._create(
            initiator=initiator, initiator_duty=initiator_duty, target=target
        )

    def accept(self) -> None:
        """
        Принять запрос на замену.

        :raises SwapRequestStatusException: Если запрос невозможно модифицировать
        :raises DutySwapException: Если текущий пользователь не имеет доступа
        :raises DutyIsLockedException: Если дежурство завершено
        """
        if not self.request_is_mutable():
            raise SwapRequestStatusException(
                "Дежурство {self._object} невозможно изменить"
            )
        if not self.is_target_user(self._user):
            raise DutySwapException(
                f"Пользователь {self._user} не может принять заявку {self}, так как она не направлена ему"
            )
        self._accept()

    def decline(self) -> None:
        """
        Отклонить запрос на замену.


        :raises SwapRequestStatusException: Если запрос невозможно модифицировать
        :raises DutySwapException: Если текущий пользователь не имеет доступа
        """
        if not self.request_is_mutable():
            raise SwapRequestStatusException(
                "Дежурство {self._object} невозможно изменить"
            )
        if not self.is_target_user(self._user):
            raise DutySwapException(
                f"Пользователь {self._user} не может отклонить заявку {self}, так как она не направлена ему"
            )
        self._decline()

    def cancel(self) -> None:
        """
        Отменить запрос на замену

        :raises SwapRequestStatusException: Если запрос невозможно модифицировать
        :raises DutySwapException: Если текущий пользователь не имеет доступа
        """
        if not self.request_is_mutable():
            raise SwapRequestStatusException(
                "Дежурство {self._object} невозможно изменить"
            )
        if not self.is_owner_user(self._user):
            raise DutySwapException(
                f"Пользователь {self._user} не может отменить заявку {self}, так как она не направлена ему"
            )
        self._cancel()

    @classmethod
    def user_is_resident(cls, user: UserModel) -> bool:
        """Проверить, является ли пользователь жителем общежития"""
        # TODO: move to user service, inject user service
        return user.is_resident

    def is_owner_user(self, user: UserModel) -> bool:
        """Проверить, является ли текущий пользователь владельцем запроса"""
        return self._object.current_user == user

    def is_target_user(self, user: UserModel) -> bool:
        """Проверить, является ли текущий пользователь целью запроса"""
        return self._object.to_swap == user

    def request_is_mutable(self) -> bool:
        """Проверить можно ли изменять запрос на замену"""
        return self._object.is_mutable

    @classmethod
    def _create(
        cls, initiator: UserModel, initiator_duty: KitchenDuty, target: UserModel
    ) -> SwapPeopleRequest:
        """Создать новый запрос на замену."""
        return SwapPeopleRequest.objects.create(
            duty=initiator_duty, current_user=initiator, to_swap=target
        )

    def _accept(self) -> None:
        """Принять запрос на замену."""
        duty_service = KitchenDutyService(self._object.duty)
        with atomic():
            self._object.accepted = True
            self._object.save()
            duty_service.swap_pupils(self._object.current_user, self._object.to_swap)

    def _decline(self) -> None:
        """Отклонить запрос на замену."""
        self._object.declined = True
        self._object.save()

    def _cancel(self) -> None:
        """Отменить запрос на замену."""
        self._object.canceled = True
        self._object.save()
