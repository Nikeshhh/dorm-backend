from datetime import date
from itertools import cycle
from abc import ABC, abstractmethod

from django.db.models import Count, Q
from django.db.transaction import atomic

from core.apps.common.exceptions import NotConfiguredException
from core.apps.common.services import get_current_year_dates
from core.apps.common.utils import date_range
from core.apps.duties.exceptions import (
    DutyIsLockedException,
    DutySwapException,
    SwapRequestStatusException,
)
from core.apps.duties.models import (
    KitchenDuty,
    KitchenDutyConfig,
    SwapDutiesRequest,
    SwapPeopleRequest,
)
from core.apps.users.exceptions import RoleViolationException
from core.apps.users.models import CustomUser as UserModel


type SwapRequest = SwapDutiesRequest | SwapPeopleRequest


def generate_duty_schedule(date_start: date, date_end: date) -> list[KitchenDuty]:
    """Создает записи дежурства на даты от :date_start до :date_end"""
    if not (config := KitchenDutyConfig.objects.first()):
        raise NotConfiguredException("Конфигурация для графиков дежурств отсутствует")
    year_start, year_end = get_current_year_dates()
    people = cycle(
        pupil
        for pupil in UserModel.objects.prefetch_related("kitchen_duties")
        .annotate(
            finished_duties_this_year=Count(
                "kitchen_duties",
                filter=Q(
                    Q(kitchen_duties__finished=True)
                    & Q(kitchen_duties__date__gte=year_start)
                    & Q(kitchen_duties__date__lte=year_end)
                ),
            )
        )
        .order_by("finished_duties_this_year", "room__number")
    )

    with atomic():
        print("Starting schedule creation")
        for day in date_range(date_start, date_end):
            duty_item = KitchenDuty.objects.create(date=day)

            for _ in range(config.people_per_day):
                duty_item.people.add(next(people))

            duty_item.save()

    print("Schedule successfully created")


class KitchenDutyService:
    def __init__(self, object: KitchenDuty):
        self._object = object

    def finish(self) -> None:
        """Завершает дежурство, запрещая его редактировать"""
        self._object.finished = True
        self._object.save()

    def swap_pupils(self, current: UserModel, new: UserModel) -> None:
        if self._object.finished:
            raise DutyIsLockedException(
                f"Дежурство {self._object} окончено и недоступно для изменения"
            )
        if current not in self._object.people.all() or new in self._object.people.all():
            raise DutySwapException(
                f"Невозможно провести замену дежурного {current} на {new}"
            )
        self._swap_pupils(current, new)

    def _swap_pupils(self, current: UserModel, new: UserModel) -> None:
        self._object.people.remove(current)
        self._object.people.add(new)
        self._object.save()


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
