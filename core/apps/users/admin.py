from django.contrib import admin

from core.apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ("surname", "name", "email")
    list_display = "pk", "name", "surname", "email"
    list_display_links = "pk", "name"
