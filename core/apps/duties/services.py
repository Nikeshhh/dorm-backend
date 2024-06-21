from datetime import date
from itertools import cycle

from django.db.models import Count, Q

from core.apps.common.exceptions import NotConfiguredException
from core.apps.common.services import get_current_year_dates
from core.apps.common.utils import date_range
from core.apps.duties.models import KitchenDuty, KitchenDutyConfig
from tests.conftest import UserModel


def generate_duty_schedule(date_start: date, date_end: date) -> list[KitchenDuty]:
    """Создает записи дежурства на даты от :date_start до :date_end"""
    if not (config := KitchenDutyConfig.objects.first()):
        raise NotConfiguredException("Конфигурация для графиков дежурств отсутствует")
    year_start, year_end = get_current_year_dates()
    people = cycle(
        pupil
        for pupil in UserModel.objects.prefetch_related("kitchen_duties")
        .annotate(
            finished_duties_this_year=Count(
                "kitchen_duties",
                filter=Q(
                    Q(kitchen_duties__finished=True)
                    & Q(kitchen_duties__date__gte=year_start)
                    & Q(kitchen_duties__date__lte=year_end)
                ),
            )
        )
        .order_by("finished_duties_this_year", "room__number")
    )

    for day in date_range(date_start, date_end):
        duty_item = KitchenDuty.objects.create(date=day)

        for _ in range(config.people_per_day):
            duty_item.people.add(next(people))

        duty_item.save()
