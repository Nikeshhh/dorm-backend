# Generated by Django 5.0.3 on 2024-05-08 10:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "proposals",
            "0002_repairproposal_executor_repairproposal_updated_at_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="repairproposal",
            name="status",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Открыта"),
                    (1, "Выполняется"),
                    (2, "Выполнена"),
                    (3, "Закрыта"),
                ],
                default=0,
                verbose_name="Статус заявки",
            ),
        ),
    ]
