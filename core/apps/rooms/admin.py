from django.contrib import admin

from core.apps.rooms.models import Block, Room, RoomRecord


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    model = Block


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    model = Room


@admin.register(RoomRecord)
class RoomRecordAdmin(admin.ModelAdmin):
    model = RoomRecord
