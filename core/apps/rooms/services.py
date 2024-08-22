from datetime import timedelta
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.exceptions import ValidationError, NotFound

from core.apps.rooms.models import Room, RoomRecord
from core.apps.users.models import CustomUser


class RoomRecordsService:
    """
    Сервис для работы с записями в книге комнаты.
    """

    def __init__(
        self, *, room_record: RoomRecord = None, current_user: CustomUser = None
    ) -> None:
        self._record = room_record
        self._user = current_user

    def get_by_id(self, id: int) -> RoomRecord:
        record = RoomRecord.objects.select_related("room").filter(id=id).first()
        if not record:
            raise NotFound("Запись не найдена")
        if self._user not in record.room.users.all() and not self._user.is_admin:
            raise PermissionError("У вас недостаточно прав для просмотра этой записи")
        return record

    def get_user_last_record(self) -> RoomRecord:
        return self.list_user_room_records().first()

    def list_user_room_records(self) -> QuerySet[RoomRecord]:
        return RoomRecord.objects.filter(room=self._user.room)

    def list_created_by_user_today(self) -> QuerySet[RoomRecord]:
        today = timezone.now().date()
        return RoomRecord.objects.filter(
            author=self._user,
            date__gte=today,
            date__lt=today + timedelta(days=1),
        )

    def update(self, grade: int, comments: str) -> RoomRecord:
        self.validate_grade(grade)
        return self._update(grade, comments)

    def _update(self, grade: int, comments: str) -> RoomRecord:
        self._record.grade = grade
        self._record.comments = comments
        self._record.save()
        return self._record

    @classmethod
    def create(
        cls, room_id: int, author: CustomUser, grade: int, comments: str
    ) -> RoomRecord:
        cls.validate_grade(grade)
        room = RoomService.get_by_id(id=room_id)
        return cls._create(room, author, grade, comments)

    @classmethod
    def _create(
        cls, room: Room, author: CustomUser, grade: int, comments: str
    ) -> RoomRecord:
        return RoomRecord.objects.create(
            room=room, author=author, grade=grade, comments=comments
        )

    @classmethod
    def validate_grade(self, grade: int) -> None:
        if not 2 <= grade <= 5:
            raise ValidationError("Оценка должна находиться в промежутке от 2 до 5")


class RoomService:
    """
    Сервис для работы с комнатами.
    """

    @classmethod
    def get_by_id(cls, id: int) -> Room:
        room = Room.objects.filter(id=id).first()
        if not room:
            raise NotFound("Комната не найдена")
        return room
