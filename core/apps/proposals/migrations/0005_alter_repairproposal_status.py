# Generated by Django 5.0.3 on 2024-05-10 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("proposals", "0004_alter_repairproposal_executor"),
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
                    (3, "Отменена"),
                ],
                default=0,
                verbose_name="Статус заявки",
            ),
        ),
    ]
