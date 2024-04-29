from datetime import date, timedelta
from typing import Generator


def date_range(date_start: date, date_end: date) -> Generator[date, date, None]:
    """Функция для создания генератора на основе дат по дням"""
    current_date = date_start
    while current_date <= date_end:
        yield current_date
        current_date += timedelta(days=1)
