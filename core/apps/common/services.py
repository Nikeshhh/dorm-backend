from datetime import date


def get_current_year_dates() -> tuple[date]:
    """Возвращает дату начала и окончания текущего учебного года"""
    today = date.today()
    start_date = date(year=today.year, month=9, day=1)
    end_date = date(year=today.year + 1, month=9, day=1)
    if today.month < 9:
        start_date = date(year=today.year - 1, month=today.month, day=today.day)
        end_date = date(year=today.year, month=today.month, day=today.day)
    return (start_date, end_date)
