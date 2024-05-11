# Generated by Django 5.0.3 on 2024-05-11 05:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("duties", "0007_swapdutiesrequest_accepted_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
