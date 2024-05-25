from datetime import date
from core.apps.common.utils import date_range


def test_date_range_generate_by_day():
    """Тестирует функцию :date_range: на предмет правильной генерации дат"""
    today_date = date.today()
    month_start = date(year=today_date.year, month=today_date.month, day=1)
    month_end = date(year=today_date.year, month=today_date.month, day=28)

    dates = []
    dates_to_test = []
    for i in range(1, 29):
        date_to_add = date(year=today_date.year, month=today_date.month, day=i)
        dates.append(date_to_add)

    for day in date_range(month_start, month_end):
        dates_to_test.append(day)

    assert dates == dates_to_test
