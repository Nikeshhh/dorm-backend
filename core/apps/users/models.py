from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from core.apps.users.managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        max_length=50, unique=True, verbose_name="Имя пользователя"
    )
    email = models.CharField(
        max_length=50, unique=True, verbose_name="Электронная почта", blank=True
    )
    surname = models.CharField(max_length=40, verbose_name="Фамилия")
    name = models.CharField(max_length=40, verbose_name="Имя")
    second_name = models.CharField(max_length=40, verbose_name="Отчество", blank=True)
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Комната проживания",
    )

    # group = models.ForeignKey(Group, verbose_name='Группа', on_delete=models.SET_NULL, null=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.surname} {self.name} {self.second_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
