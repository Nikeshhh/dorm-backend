from django.db.transaction import atomic

from core.apps.duties.exceptions import DutySwapException, SwapRequestStatusException
from core.apps.duties.models import KitchenDuty, SwapDutiesRequest
from core.apps.duties.services import BaseSwapRequestService, KitchenDutyService
from core.apps.users.exceptions import RoleViolationException
from core.apps.users.models import CustomUser as UserModel


class SwapDutiesService(BaseSwapRequestService):
    """
    Сервис для работы с заявками на обмен дежурствами.
    """

    def __init__(self, current_user: UserModel, object: SwapDutiesRequest) -> None:
        """
        :param current_user: Текущий пользователь при работе сервиса.
        :param object: Объекта запроса на обмен дежурствами.
        """
        self._object = object
        self._user = current_user

    @classmethod
    def get_by_id(cls, id: int) -> SwapDutiesRequest:
        return SwapDutiesRequest.objects.get(id=id)

    @classmethod
    def create(
        cls,
        initiator: UserModel,
        initiator_duty: KitchenDuty,
        target: UserModel,
        target_duty: KitchenDuty,
    ) -> SwapDutiesRequest:
        """
        Создать запрос на обмен дежурствами.

        :param initiator: Пользователь, который создает запрос.
        :param initiator_duty: Дежурство инициатора заявки.
        :param target: Пользователь, которому направлен запрос.
        :param target_duty: Дежурство, на которое направлен запрос.
        """
        if not cls.user_is_resident(initiator) or not cls.user_is_resident(target):
            raise RoleViolationException("Пользователи должны быть жителями общежития")
        if initiator == target:
            raise DutySwapException(
                "Невозможно создать заявку на обмен между идентичными пользователями"
            )
        if initiator_duty == target_duty:
            raise DutySwapException(
                "Невозможно создать заявку на обмен между идентичными дежурствами"
            )
        return cls._create(initiator, initiator_duty, target, target_duty)

    def accept(self) -> None:
        """
        Принять запрос на обмен дежурствами.

        :param user: Пользователь, который принимает запрос. Используется для валидации.
        :raises SwapRequestStatusException: Если статус запроса не позволяет принять его.
        :raises DutySwapException: Если запрос не направлен пользователю.
        """
        if not self.request_is_mutable():
            raise SwapRequestStatusException(
                "Невозможно принять заявку из-за ее текущего статуса"
            )
        if not self.is_target_user(self._user):
            raise DutySwapException(
                f"Пользователь {self._user} не может принять заявку {self._object}, так как не имеет к ней доступа"
            )
        self._swap_duties()

    def cancel(self) -> None:
        """
        Отменить запрос на обмен дежурствами.

        :param owner: Владелец заявки. Используется для валидации.
        :raises SwapRequestStatusException: Если статус запроса не позволяет отменить его.
        """
        if not self.request_is_mutable():
            raise SwapRequestStatusException(
                "Невозможно отклонить запрос из-за его текущего статуса"
            )
        if not self.is_owner_user(self._user):
            raise DutySwapException(
                f"Пользователь {self._user} не может отменить запрос {self._object}, так как не имеет к ней доступа"
            )
        self._cancel()

    def decline(self) -> None:
        """
        Отклонить запрос на обмен дежурствами.

        :param user: Пользователь, который отклоняет запрос. Используется для валидации.
        :raises SwapRequestStatusException: Если статус запроса не позволяет отклонить его.
        :raise DutySwapException: Если запрос не направлен пользователю.
        """
        if not self.request_is_mutable():
            raise SwapRequestStatusException(
                "Невозможно отклонить запрос из-за его текущего статуса"
            )
        if not self.is_target_user(self._user):
            raise DutySwapException(
                f"Пользователь {self._user} не может отклонить заявку {self._object}, так как не имеет к ней доступа"
            )
        self._decline()

    def is_target_user(self, user: UserModel) -> bool:
        """Проверить, является ли пользователь целью запроса"""
        return self._object.second_user == user

    def is_owner_user(self, user: UserModel) -> bool:
        """Проверить, является ли пользователь владельцем запроса"""
        return self._object.first_user == user

    def request_is_mutable(self) -> bool:
        """Проверить, можно ли изменять запрос"""
        return self._object.is_mutable

    @classmethod
    def user_is_resident(cls, user: UserModel) -> bool:
        """Проверить, является ли пользователь жителем общежития"""
        # TODO: move to user service, inject user service
        return user.is_resident

    @classmethod
    def _create(
        cls,
        initiator: UserModel,
        initiator_duty: KitchenDuty,
        target: UserModel,
        target_duty: KitchenDuty,
    ) -> SwapDutiesRequest:
        return SwapDutiesRequest.objects.create(
            first_duty=initiator_duty,
            first_user=initiator,
            second_duty=target_duty,
            second_user=target,
        )

    def _cancel(self):
        """Отменить запрос на обмен дежурствами"""
        self._object.canceled = True
        self._object.save()

    def _decline(self):
        """Отклонить запрос на обмен дежурствами"""
        self._object.declined = True
        self._object.save()

    def _swap_duties(self) -> None:
        """Произвести обмен дежурствами"""
        initiator_duty_service = KitchenDutyService(self._object.first_duty)
        target_duty_service = KitchenDutyService(self._object.second_duty)
        with atomic():
            initiator_duty_service._swap_pupils(
                self._object.first_user, self._object.second_user
            )
            target_duty_service._swap_pupils(
                self._object.second_user, self._object.first_user
            )
            self._object.accepted = True
            self._object.save()
