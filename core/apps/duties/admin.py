from django.contrib import admin

from core.apps.duties.models import KitchenDuty  # noqa


@admin.register(KitchenDuty)
class KitchenDutyAdmin(admin.ModelAdmin):
    model = KitchenDuty
