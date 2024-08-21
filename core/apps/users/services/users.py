from core.apps.users.models import CustomUser


class UserService:
    @classmethod
    def get_by_id(cls, id: int) -> CustomUser:
        return CustomUser.objects.get(id=id)

    @classmethod
    def get_all_residents(cls):
        return CustomUser.objects.filter(resident=True)
