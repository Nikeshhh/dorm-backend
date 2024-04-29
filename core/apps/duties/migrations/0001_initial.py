# Generated by Django 5.0.3 on 2024-04-29 08:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="KitchenDuty",
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
                ("date", models.DateField(verbose_name="Дата дежурства")),
                (
                    "finished",
                    models.BooleanField(default=False, verbose_name="Завершено?"),
                ),
                (
                    "people",
                    models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL, verbose_name="Ответственные"
                    ),
                ),
            ],
            options={
                "verbose_name": "Дежурство по кухням",
                "verbose_name_plural": "Дежурства по кухням",
            },
        ),
    ]
