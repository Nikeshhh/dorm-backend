from django.contrib import admin

from core.apps.duties.models import KitchenDuty, SwapDutiesRequest, SwapPeopleRequest  # noqa


@admin.register(KitchenDuty)
class KitchenDutyAdmin(admin.ModelAdmin):
    model = KitchenDuty


@admin.register(SwapPeopleRequest)
class SwapPeopleRequestAdmin(admin.ModelAdmin):
    model = SwapPeopleRequest


@admin.register(SwapDutiesRequest)
class SwapDutiesRequestAdmin(admin.ModelAdmin):
    model = SwapDutiesRequest
