# Generated by Django 5.0.3 on 2024-06-25 09:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0003_alter_roomrecord_author"),
    ]

    operations = [
        migrations.AlterField(
            model_name="roomrecord",
            name="date",
            field=models.DateTimeField(verbose_name="Дата и время записи"),
        ),
    ]
