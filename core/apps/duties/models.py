from django.contrib.auth import get_user_model
from django.db import models
from django.db.transaction import atomic

from core.apps.common.validators import user_is_resident
from core.apps.duties.exceptions import (
    DutyIsLockedException,
    DutySwapException,
    SwapRequestStatusException,
)
from core.apps.users.exceptions import RoleViolationException
from core.apps.users.models import CustomUser


UserModel = get_user_model()


class KitchenDutyConfig(models.Model):
    """Настройки для дежурств"""

    people_per_day = models.SmallIntegerField(
        verbose_name="Количество человек на 1 день дежурства"
    )


class KitchenDuty(models.Model):
    """Дежурства по кухням"""

    date = models.DateField(verbose_name="Дата дежурства")
    people = models.ManyToManyField(
        UserModel,
        verbose_name="Ответственные",
        related_name="kitchen_duties",
        validators=[user_is_resident],
    )
    finished = models.BooleanField(verbose_name="Завершено?", default=False)

    class Meta:
        verbose_name = "Дежурство по кухням"
        verbose_name_plural = "Дежурства по кухням"

    def __str__(self) -> str:
        return f'{self.date}: {(', '.join(str(pupil) for pupil in self.people.all()))}'

    def finish(self) -> None:
        self.finished = True
        self.save()

    def swap_pupils(self, current: CustomUser, new: CustomUser) -> None:
        if self.finished:
            raise DutyIsLockedException("Дежурство окончено и недоступно для изменения")
        if current not in self.people.all() or new in self.people.all():
            raise DutySwapException(
                f"Невозможно провести замену дежурного {current} на {new}"
            )

        self.people.remove(current)
        self.people.add(new)
        self.save()


class SwapDutiesRequest(models.Model):
    """Заявка на обмен дежурствами"""

    first_duty = models.ForeignKey(
        KitchenDuty,
        on_delete=models.CASCADE,
        verbose_name="Дежурство инициатора заявки",
        related_name="initialized_swap_duties_requests",
    )
    first_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Инициатор заявки",
        related_name="initialized_swap_duties_requests",
    )
    second_duty = models.ForeignKey(
        KitchenDuty,
        on_delete=models.CASCADE,
        verbose_name="Дежурство цели заявки",
        related_name="addressed_swap_duties_requests",
    )
    second_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Цель заявки",
        related_name="addressed_swap_duties_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    accepted = models.BooleanField(default=False, verbose_name="Принята?")
    declined = models.BooleanField(default=False, verbose_name="Отклонена?")
    canceled = models.BooleanField(default=False, verbose_name="Отменена?")

    def accept(self, user: CustomUser):
        if not self.is_mutable:
            raise SwapRequestStatusException
        if self.second_user != user:
            raise DutySwapException(
                f"Пользователь {user} не может принять заявку {self}, так как не имеет к ней доступа"
            )
        with atomic():
            self.first_duty.swap_pupils(self.first_user, self.second_user)
            self.second_duty.swap_pupils(self.second_user, self.first_user)
            self.accepted = True
            self.save()

    def decline(self, user: CustomUser):
        if not self.is_mutable:
            raise SwapRequestStatusException
        if self.second_user != user:
            raise DutySwapException(
                f"Пользователь {user} не может отклонить заявку {self}, так как не имеет к ней доступа"
            )
        self.declined = True
        self.save()

    @property
    def is_mutable(self):
        return not (self.canceled or self.declined or self.accepted)

    def cancel(self, user: CustomUser):
        if not self.is_mutable:
            raise SwapRequestStatusException
        if self.first_user != user:
            raise DutySwapException(
                f"Пользователь {user} не может отменить заявку {self}, так как не является ее инициатором"
            )
        self.canceled = True
        self.save()

    def save(self, *args, **kwargs) -> None:
        if not self.first_user.is_resident or not self.second_user.is_resident:
            raise RoleViolationException
        if self.first_duty == self.second_duty:
            raise DutySwapException(
                "Невозможно создать заявку на обмен между идентичными дежурствами"
            )
        if self.first_user == self.second_user:
            raise DutySwapException(
                "Невозможно создать заявку на обмен между идентичными пользователями"
            )
        return super().save(*args, **kwargs)


class SwapPeopleRequest(models.Model):
    """Заявка на замену одного дежурного на другого"""

    duty = models.ForeignKey(
        KitchenDuty, on_delete=models.CASCADE, related_name="swap_people_requests"
    )
    current_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="initialized_swap_people_requests",
    )
    to_swap = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="addressed_swap_people_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    accepted = models.BooleanField(default=False, verbose_name="Принята?")
    declined = models.BooleanField(default=False, verbose_name="Отклонена?")
    canceled = models.BooleanField(default=False, verbose_name="Отменена?")

    def accept(self, user: CustomUser):
        if not self.is_mutable:
            raise SwapRequestStatusException
        if self.to_swap != user:
            raise DutySwapException(
                f"Пользователь {user} не может принять заявку {self}, так как не имеет к ней доступа"
            )
        self.accepted = True
        self.save()
        self.duty.swap_pupils(self.current_user, self.to_swap)

    def decline(self, user: CustomUser):
        if not self.is_mutable:
            raise SwapRequestStatusException
        if self.to_swap != user:
            raise DutySwapException(
                f"Пользователь {user} не может отклонить заявку {self}, так как не имеет к ней доступа"
            )
        self.declined = True
        self.save()

    def cancel(self, user: CustomUser):
        if not self.is_mutable:
            raise SwapRequestStatusException
        if self.current_user != user:
            raise DutySwapException(
                f"Пользователь {user} не может отменить заявку {self}, так как не является ее инициатором"
            )
        self.canceled = True
        self.save()

    @property
    def is_mutable(self):
        return not (self.canceled or self.declined or self.accepted)

    def save(self, *args, **kwargs) -> None:
        if not self.current_user.is_resident or not self.to_swap.is_resident:
            raise RoleViolationException
        if self.current_user not in self.duty.people.all():
            raise DutySwapException(
                f"Дежурный {self.current_user} не принадлежит дежурству {self.duty}"
            )
        if self.to_swap in self.duty.people.all():
            raise DutySwapException(
                f"Дежурный {self.to_swap} уже принадлежит дежурству {self.duty}"
            )
        if self.current_user == self.to_swap:
            raise DutySwapException(
                "Невозможно создать заявку на обмен между идентичными пользователями"
            )
        return super().save(*args, **kwargs)
