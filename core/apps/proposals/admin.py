from django.contrib import admin

from core.apps.proposals.models import RepairProposal


@admin.register(RepairProposal)
class RepairProposalAdmin(admin.ModelAdmin):
    list_filter = ("status",)
    list_display = (
        "get_number",
        "description",
        "get_author",
        "status",
    )
    list_display_links = (
        "get_number",
        "description",
        "get_author",
        "status",
    )
    search_fields = (
        "description",
        "status",
    )
    model = RepairProposal

    @admin.display(description="Автор")
    def get_author(self, obj) -> str:
        return f"{obj.author.surname} {obj.author.room.number}"

    @admin.display(description="Номер заявки")
    def get_number(self, obj) -> str:
        return f"Номер {obj.pk}"
