from core.apps.users.models import CustomUser


class UserService:
    """
    Сервис для работы с пользователями.
    """

    @classmethod
    def get_by_id(cls, id: int) -> CustomUser:
        """
        Получить пользователя по идентификатору.

        :param id: идентификатор пользователя
        :return: Пользователь
        :raises User.DoesNotExist: Если пользователь не найден
        """
        return CustomUser.objects.get(id=id)

    @classmethod
    def get_all_residents(cls):
        """
        Получить всех проживающих.

        :return: QuerySet со всеми проживающими
        """
        return CustomUser.objects.filter(resident=True)
