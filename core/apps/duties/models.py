from django.contrib.auth import get_user_model
from django.db import models


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
        UserModel, verbose_name="Ответственные", related_name="kitchen_duties"
    )
    finished = models.BooleanField(verbose_name="Завершено?", default=False)

    class Meta:
        verbose_name = "Дежурство по кухням"
        verbose_name_plural = "Дежурства по кухням"

    def __str__(self) -> str:
        return f'{self.date}: {(', '.join(str(pupil) for pupil in self.people.all()))}'
