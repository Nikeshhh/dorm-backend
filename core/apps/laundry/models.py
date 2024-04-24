from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class LaundryRecord(models.Model):
    record_date = models.DateField(verbose_name="Дата записи")
    time_start = models.TimeField(verbose_name="Начало записи")
    time_end = models.TimeField(verbose_name="Окончание записи")
    owner = models.ForeignKey(
        UserModel,
        verbose_name="Чья запись",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Запись прачечной"
        verbose_name_plural = "Записи прачечной"

    def __str__(self) -> str:
        return f"{self.time_start}-{self.time_end}"

    @property
    def is_available(self) -> bool:
        return not self.owner


class LaundryRecordTemplate(models.Model): ...


class LaundryScheduleTemplate(models.Model): ...
