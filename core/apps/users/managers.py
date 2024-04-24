from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        username=None,
        password=None,
        is_active=True,
        is_staff=False,
        is_admin=False,
    ):
        user_obj = self.model(username=username)
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
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
