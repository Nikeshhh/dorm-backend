import csv
from datetime import datetime
from string import ascii_letters
from random import choices

from django.db.transaction import atomic
from core.apps.rooms.models import Room
from core.apps.users.models import CustomUser


translit_dict = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ы": "y",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def get_username(lastname: str, firstname: str, second_name: str, *, index: int) -> str:
    idx = (4 - len(str(index))) * "0" + str(index)
    postfix = f"2024{idx}"
    return (
        f"{translit_dict.get(lastname.lower()[0])}"
        f"{translit_dict.get(firstname.lower()[0])}"
        f"{translit_dict.get(second_name.lower()[0])}"
        f"{postfix}"
    )


def get_random_password(length: int = 8) -> str:
    symbols = ascii_letters + "0123456789"
    return "".join(choices(symbols, k=length))


def import_users_from_csv(filename: str):
    if filename[-4:] != ".csv":
        raise ValueError("Неправильный формат файла")
    with atomic():
        today = datetime.today().strftime("%d.%m.%Y")
        with open(filename, "r", encoding="utf-8") as file:
            with open(
                f"users_output_{today}.csv", "w", encoding="windows-1251"
            ) as output_file:
                writer = csv.writer(output_file, delimiter=";")
                writer.writerow(
                    ["Фамилия", "Имя", "Отчество", "Имя пользователя", "Пароль"]
                )

                reader = csv.reader(file, delimiter=";")
                next(reader)
                for i, row in enumerate(reader):
                    password = get_random_password()
                    username = get_username(*row[:3], index=i)
                    room = Room.objects.get(number=row[4])
                    CustomUser.objects.create_user(
                        is_resident=True,
                        username=username,
                        password=password,
                        surname=row[0],
                        name=row[1],
                        second_name=row[2],
                        room=room,
                    )
                    output_data = [*row[:3], username, password]
                    writer.writerow(output_data)
