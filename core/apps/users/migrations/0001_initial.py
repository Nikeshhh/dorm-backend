# Generated by Django 5.0.3 on 2024-04-24 13:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Имя пользователя"
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        unique=True,
                        verbose_name="Электронная почта",
                    ),
                ),
                ("surname", models.CharField(max_length=40, verbose_name="Фамилия")),
                ("name", models.CharField(max_length=40, verbose_name="Имя")),
                (
                    "second_name",
                    models.CharField(
                        blank=True, max_length=40, verbose_name="Отчество"
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("staff", models.BooleanField(default=False)),
                ("admin", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
