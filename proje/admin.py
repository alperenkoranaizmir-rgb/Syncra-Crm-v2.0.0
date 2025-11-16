from django.contrib import admin

from proje.models import Agreement, Document, Owner, Ownership, Project, Unit


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "status", "manager")
    search_fields = ("code", "name", "location")
    list_filter = ("status", "type")


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "tc_no", "phone")
    search_fields = ("first_name", "last_name", "tc_no")


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("project", "ada", "parsel", "type", "agreement_status")
    list_filter = ("type", "agreement_status")
    search_fields = ("ada", "parsel", "address")


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ("unit", "owner", "share_percent", "status")


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ("unit", "date", "status", "staff")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "project", "unit", "uploaded_by", "uploaded_at")
