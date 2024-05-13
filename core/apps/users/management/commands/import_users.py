from typing import Any
from django.core.management.base import BaseCommand, CommandParser

from core.apps.users.services import import_users_from_csv


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("filename", type=str)

    def handle(self, *args: Any, **options: Any) -> str | None:
        import_users_from_csv(filename=options["filename"])
        self.stdout.write(self.style.SUCCESS("Пользователи успешно импортированы"))
