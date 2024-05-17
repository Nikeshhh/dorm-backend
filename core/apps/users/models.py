from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from core.apps.users.managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        max_length=50, unique=True, verbose_name="Имя пользователя"
    )
    email = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Электронная почта",
        blank=True,
        null=True,
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

    active = models.BooleanField(default=True)
    resident = models.BooleanField(default=True)  # проживающий
    staff = models.BooleanField(default=False)  # член студсовета
    admin = models.BooleanField(default=False)  # администратор
    worker = models.BooleanField(default=False)  # работник

    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        fio = f"{self.surname} {self.name} {self.second_name}"
        return fio if fio.strip() else self.username

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

    @property
    def is_worker(self):
        return self.worker

    @property
    def is_resident(self):
        return self.resident
