# Generated by Django 5.0.3 on 2024-04-29 11:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("duties", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="KitchenDutyConfig",
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
                (
                    "people_per_day",
                    models.SmallIntegerField(
                        verbose_name="Количество человек на 1 день дежурства"
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="kitchenduty",
            name="people",
            field=models.ManyToManyField(
                related_name="kitchen_duties",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Ответственные",
            ),
        ),
    ]
