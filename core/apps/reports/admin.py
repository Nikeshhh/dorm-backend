from datetime import datetime, timedelta
from django.contrib import admin
from django.urls import path

from core.apps.duties.admin import (
    KitchenDuty,
    KitchenDutyAdmin,
    SwapDutiesRequest,
    SwapDutiesRequestAdmin,
)
from core.apps.laundry.admin import LaundryRecord, LaundryRecordAdmin
from core.apps.proposals.admin import RepairProposal, RepairProposalAdmin
from core.apps.reports.services import get_report_file_reponse
from core.apps.rooms.admin import Room, RoomAdmin, RoomRecord, RoomRecordAdmin
from core.apps.users.admin import CustomUser, CustomUserAdmin


class MyAdminSite(admin.AdminSite):
    site_header = "Общежитие № 20"
    index_template = "reports/index.html"
    index_title = "Администрирование"
    room_record_report_template = "reports/room_records_report.html"
    duty_schedule_report_template = "reports/duty_schedule_report.html"
    days_converter = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье",
    }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "room-records-report/",
                self.admin_view(self.get_room_record_report),
                name="room-records-report",
            ),
            path(
                "duty-schedule-report/",
                self.admin_view(self.get_duty_schedule_report),
                name="duty-schedule-report",
            ),
        ]
        return custom_urls + urls

    def get_room_record_report(self, request):
        report_date = datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
        records_with_violations = RoomRecord.objects.filter(
            grade__lt=5,
            date__gte=report_date,
            date__lte=report_date + timedelta(days=1),
        )
        context = {
            "result": [
                {"room_number": rec.room.number, "comments": rec.comments}
                for rec in records_with_violations
            ],
            "date": report_date.strftime("%d.%m.%Y"),
        }
        response = get_report_file_reponse(
            request=request,
            template_name=self.room_record_report_template,
            context=context,
            base_filename="sanitary_violations_report",
            filename_postfix=f'{report_date.strftime('%d.%m.%Y')}',
        )
        return response

    def get_duty_schedule_report(self, request):
        date_start = datetime.strptime(request.POST.get("week") + "-1", "%Y-W%W-%w")
        date_end = date_start + timedelta(days=7)
        duty_records = KitchenDuty.objects.filter(
            date__gte=date_start, date__lte=date_end
        ).order_by("date")
        context = {
            "date_start": date_start.strftime("%d.%m.%Y"),
            "date_end": date_end.strftime("%d.%m.%Y"),
            "result": [
                {
                    "date": rec.date,
                    "day": self.days_converter[rec.date.strftime("%A")],
                    "people": [
                        {"name": person.short_name, "room_number": person.room.number}
                        for person in rec.people.all()
                    ],
                    "people_amount": rec.people.count() + 1,
                    "time": "09:00-23:00"
                    if rec.date.strftime("%A") in ["Saturday", "Sunday"]
                    else "16:00-23:00",
                }
                for rec in duty_records
            ],
        }
        response = get_report_file_reponse(
            request=request,
            template_name=self.duty_schedule_report_template,
            context=context,
            base_filename="duty_schedule_report",
            filename_postfix=f'{date_start.strftime('%d.%m.%Y')}-{date_end.strftime('%d.%m.%Y')}',
        )
        return response

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["room_record_report_button"] = True
        extra_context["duty_schedule_report_button"] = True
        return super().index(request, extra_context=extra_context)


admin_site = MyAdminSite(name="myadmin")


admin_site.register(KitchenDuty, KitchenDutyAdmin)
admin_site.register(SwapDutiesRequest, SwapDutiesRequestAdmin)
admin_site.register(LaundryRecord, LaundryRecordAdmin)
admin_site.register(RepairProposal, RepairProposalAdmin)
admin_site.register(Room, RoomAdmin)
admin_site.register(RoomRecord, RoomRecordAdmin)
admin_site.register(CustomUser, CustomUserAdmin)
