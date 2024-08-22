from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from core.apps.laundry.exceptions import RecordStateException
from core.apps.laundry.models import LaundryRecord
from core.apps.users.models import CustomUser


class LaundryService:
    """
    Сервис для работы с заявками в журнале прачечной.
    """

    def __init__(self, current_user: CustomUser, record: LaundryRecord) -> None:
        """
        :param current_user: Текущий пользователь при работе сервиса.
        :param record: Текущая запись при работе сервиса.
        """
        self._record = record
        self._user = current_user

    @classmethod
    def get_by_id(cls, id: int) -> LaundryRecord:
        """
        Получить запись по ID.

        :param id: ID записи.
        :raises LaundryRecord.DoesNotExist: Если запись не найдена.
        :returns: LaundryRecord с переданным ID.
        """
        return LaundryRecord.objects.get(id=id)

    @classmethod
    def get_users_records(cls, user: CustomUser) -> list:
        """
        Получить записи, зарезервированные пользователем.

        :param user: Пользователь для фильтрации.
        :returns: QuerySet[LaundryRecord] Записи пользователя.
        """
        return LaundryRecord.objects.filter(owner=user)

    @classmethod
    def get_users_records_today(cls, user: CustomUser) -> list:
        """
        Получить сегодняшние записи, зарезервированные пользователем.

        :param user: Пользователь для фильтрации.
        :returns: QuerySet[LaundryRecord] Сегодняшние записи пользователя.
        """
        today = timezone.now().date()
        return cls.get_users_records(user).filter(record_date=today)

    @classmethod
    def get_today_records_stats(cls) -> str:
        """
        Получить статистику свободных записей на сегодня.

        :returns: str Статистика свободных записей.
        """
        records_count = cls.get_today_records_count()
        if records_count > 0:
            message = f"Свободно {records_count} записей"
        else:
            message = "На сегодня нет свободных записей"
        return message

    @classmethod
    def get_today_records_count(cls) -> int:
        """
        Получить количество свободных записей на сегодня.

        :returns: int Количество свободных записей.
        """
        today = timezone.now().date()
        return LaundryRecord.objects.filter(owner=None, record_date=today).count()

    def take_record(self) -> None:
        """
        Зарезервировать запись.

        :raises RecordStateException: Если запись уже занята.
        """
        if not self._record.is_available:
            raise RecordStateException("Запись уже занята")
        self._set_owner()

    def _set_owner(self) -> None:
        """Установить текущего пользователя в качестве владельца текущей записи."""
        self._record.owner = self._user
        self._record.save()

    def free_record(self) -> None:
        """
        Освободить запись.

        :raises RecordStateException: Если запись уже свободна.
        :raises PermissionDenied: Если текущий пользователь не является владельцем записи.
        """
        if self._record.is_available:
            raise RecordStateException("Запись уже свободна")
        if not self.is_owner_user():
            raise PermissionDenied("Запись вам не принадлежит")
        self._remove_owner()

    def _remove_owner(self) -> None:
        """Удалить владельца текущей записи."""
        self._record.owner = None
        self._record.save()

    def is_owner_user(self) -> bool:
        """Проверить, является ли текущий пользователь владельцем текущей записи."""
        return self._record.owner == self._user
