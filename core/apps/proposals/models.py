from django.db import models

from core.apps.common.validators import user_is_worker
from core.apps.proposals.choices import PROPOSAL_STATUS_CHOICES
from core.apps.proposals.exceptions import (
    ProposalAccessException,
    ProposalStatusException,
)
from core.apps.rooms.exceptions import NoRoomException
from core.apps.users.exceptions import RoleViolationException
from core.apps.users.models import CustomUser


class RepairProposal(models.Model):
    author = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Автор заявки",
        related_name="repair_proposals",
    )
    description = models.TextField(verbose_name="Описание проблемы")
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус заявки",
        choices=PROPOSAL_STATUS_CHOICES,
        default=0,
    )
    updated_at = models.DateTimeField(
        verbose_name="Последнее обновление",
        auto_now=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Создана",
        auto_now_add=True,
    )
    executor = models.ForeignKey(
        "users.CustomUser",
        verbose_name="Исполнитель заявки",
        on_delete=models.SET_NULL,
        validators=[user_is_worker],
        null=True,
    )

    class Meta:
        verbose_name = "Заявка на ремонт"
        verbose_name_plural = "Заявки на ремонт"

    def __str__(self) -> str:
        return f"Заявка номер {self.pk}. Статус: {self.get_status_display()}"

    def refuse(self, author: CustomUser):
        # Недоступна для заявок со статусом "Выполнена" (2)
        if self.author != author:
            raise ProposalAccessException(f"{author} не имеет доступа к заявке {self}")
        if self.status == 2:
            raise ProposalStatusException(f"Невозможно отказаться от {self}")
        self.status = 3
        self.save()

    def accept(self, executor: CustomUser) -> None:
        # Доступно только для заявок со статусом "Открыта" (0)
        if not executor.is_worker:
            raise RoleViolationException
        if self.executor:
            if self.executor == executor:
                raise ProposalStatusException(
                    f"{executor} не может повторно принять заявку"
                )
            raise ProposalAccessException(
                f"{executor} не может принять заявку {self}, так как она уже занята {self.executor}"
            )
        if self.status != 0:
            raise ProposalStatusException(f"{self} не доступна для принятия")
        self.status = 1
        self.executor = executor
        self.save()

    def decline(self, executor: CustomUser) -> None:
        # Доступно только для заявок со статусом "Выполняется" (1)
        if not executor.is_worker:
            raise RoleViolationException
        if self.executor != executor:
            raise ProposalAccessException(
                f"{executor} не имеет доступа к заявке {self}"
            )
        if self.status != 1:
            raise ProposalStatusException(f"{self} не может быть отменена")
        self.status = 0
        self.executor = None
        self.save()

    def close(self, executor: CustomUser) -> None:
        # Доступоно только для заявок со статусом "Выполняется" (1)
        if self.executor != executor:
            raise ProposalAccessException(
                f"{executor} не имеет доступа к заявке {self}"
            )
        if self.status != 1:
            raise ProposalStatusException(f"{self} не может быть закрыта")
        self.status = 2
        self.save()

    def save(self, *args, **kwargs):
        if not self.author.is_resident:
            raise RoleViolationException
        if self.author.room is None:
            raise NoRoomException
        return super().save(*args, **kwargs)
