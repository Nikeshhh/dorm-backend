from django.contrib import admin

from core.apps.proposals.models import RepairProposal


@admin.register(RepairProposal)
class RepairProposalAdmin(admin.ModelAdmin):
    model = RepairProposal
