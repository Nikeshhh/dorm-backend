from core.apps.duties.exceptions import DutyIsLockedException, DutySwapException
from core.apps.duties.models import KitchenDuty
from core.apps.users.models import CustomUser as UserModel


class KitchenDutyService:
    def __init__(self, object: KitchenDuty):
        self._object = object

    @classmethod
    def get_by_id(cls, id: int) -> KitchenDuty:
        return KitchenDuty.objects.get(id=id)

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
