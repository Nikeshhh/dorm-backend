from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        username=None,
        password=None,
        surname="",
        name="",
        second_name="",
        is_resident=False,
        is_active=True,
        is_staff=False,
        is_admin=False,
        is_worker=False,
        room=None,
    ):
        user_obj = self.model(username=username)
        user_obj.set_password(password)
        user_obj.surname = surname
        user_obj.name = name
        user_obj.second_name = second_name
        user_obj.resident = is_resident
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.worker = is_worker
        user_obj.room = room
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user
