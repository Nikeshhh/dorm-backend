# Generated by Django 5.0.3 on 2024-05-10 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("duties", "0006_swapdutiesrequest_canceled_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="swapdutiesrequest",
            name="accepted",
            field=models.BooleanField(default=False, verbose_name="Принята?"),
        ),
        migrations.AddField(
            model_name="swappeoplerequest",
            name="accepted",
            field=models.BooleanField(default=False, verbose_name="Принята?"),
        ),
    ]