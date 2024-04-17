from django.contrib import admin

from core.apps.laundry.models import LaundryRecord


@admin.register(LaundryRecord)
class LaundryRecordAdmin(admin.ModelAdmin):
    list_display = (
        'record_date',
        'time_start',
        'time_end',
        'is_available'
    )
    list_display_links = (
        'record_date',
        'time_start',
        'time_end',
    )