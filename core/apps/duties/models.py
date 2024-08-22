from django.contrib.auth import get_user_model
from django.db import models

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
    )
    finished = models.BooleanField(verbose_name="Завершено?", default=False)

    class Meta:
        verbose_name = "Дежурство по кухням"
        verbose_name_plural = "Дежурства по кухням"

    def __str__(self) -> str:
        return f'{self.date}: {(', '.join(str(pupil) for pupil in self.people.all()))}'

    def finish(self):
        """Завершить дежурство, только для удобства тестов"""
        self.finished = True
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

    @property
    def is_mutable(self) -> bool:
        return not self.accepted and not self.declined and not self.canceled

    class Meta:
        verbose_name = "Запрос на обмен"
        verbose_name_plural = "Запросы на обмен"


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

    @property
    def is_mutable(self):
        return not (self.canceled or self.declined or self.accepted)
