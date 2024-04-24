from django.db import models

from core.apps.rooms.choices import ROOM_GRADE_CHOICES
from core.apps.users.models import CustomUser


class Block(models.Model):
    floor = models.IntegerField(verbose_name="Номер этажа")

    def __str__(self) -> str:
        return f'{', '.join((str(room) for room in self.rooms.all()))}'

    class Meta:
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"


class Room(models.Model):
    number = models.CharField(verbose_name="Номер комнаты", max_length=10)
    block = models.ForeignKey(
        Block, on_delete=models.PROTECT, verbose_name="Блок", related_name="rooms"
    )

    def __str__(self) -> str:
        return f"Этаж: {self.block.floor} Номер: {self.number}"

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"


class RoomRecord(models.Model):
    date = models.DateTimeField(verbose_name="Дата и время записи", auto_now_add=True)
    grade = models.PositiveSmallIntegerField(
        verbose_name="Оценка", choices=ROOM_GRADE_CHOICES
    )
    comments = models.TextField(verbose_name="Замечания", default="Замечаний нет")
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name="Комната",
        related_name="room_records",
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Ответственный"
    )

    def __str__(self) -> str:
        return f'{self.room} - {self.date.strftime('%d.%m.%Y %H:%M')}. Оценка: {self.grade}'

    class Meta:
        verbose_name = "Запись в книге комнаты"
        verbose_name_plural = "Записи в книге комнаты"
