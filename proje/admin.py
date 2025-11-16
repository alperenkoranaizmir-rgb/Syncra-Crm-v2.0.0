import csv
import json
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render

from proje.models import Agreement, Document, Owner, Ownership, Project, Unit

from .utils import generate_report_path


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "status", "manager")
    search_fields = ("code", "name", "location")
    list_filter = ("status", "type")


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "tc_no", "phone")
    search_fields = ("first_name", "last_name", "tc_no")
    actions = ["assign_group_to_owner_users"]

    # Provide an action form to pick a group
    class GroupAssignActionForm(forms.Form):
        group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    action_form = GroupAssignActionForm

    @admin.action(description="Assign selected owners (by email) to a Group")
    def assign_group_to_owner_users(self, request, queryset):
        """Admin action with confirmation form. Shows a confirmation page where admin
        can choose the Group, toggle dry-run, and optionally provide a report file path.
        On confirmation the selected owners are matched by `email` to Users and assigned.
        """
        # If this is the confirmation POST, perform assignment
        if request.method == "POST" and request.POST.get("confirm"):
            group_pk = request.POST.get("group")
            dry_run = request.POST.get("dry_run") == "on"
            report_file = request.POST.get("report_file") or ""
            report_format = request.POST.get("report_format") or "csv"

            group = Group.objects.filter(pk=group_pk).first()
            if not group:
                self.message_user(
                    request, "No group selected", level=admin.messages.ERROR
                )
                return None

            User = get_user_model()
            report_rows = []
            assigned = 0
            for owner in queryset:
                ident = (owner.email or "").strip()
                if not ident:
                    report_rows.append({"ident": str(owner), "status": "no_email"})
                    continue
                user = User.objects.filter(email__iexact=ident).first()
                if not user:
                    report_rows.append({"ident": ident, "status": "not_found"})
                    continue
                if dry_run:
                    report_rows.append(
                        {
                            "ident": ident,
                            "user": str(user),
                            "group": str(group),
                            "status": "would_assign",
                        }
                    )
                else:
                    group.user_set.add(user)
                    assigned += 1
                    report_rows.append(
                        {
                            "ident": ident,
                            "user": str(user),
                            "group": str(group),
                            "status": "assigned",
                        }
                    )

            # if no report_file provided but we have report_rows, generate auto-named path
            if not report_file and report_rows:
                report_file = generate_report_path(
                    prefix="reports/owners_assign", ext=report_format
                )

            # write report if requested
            if report_file:
                p = Path(report_file)
                p.parent.mkdir(parents=True, exist_ok=True)
                if report_format == "csv":
                    keys = ["ident", "user", "group", "status"]
                    with p.open("w", newline="", encoding="utf-8") as outfh:
                        writer = csv.DictWriter(outfh, fieldnames=keys)
                        writer.writeheader()
                        for r in report_rows:
                            writer.writerow({k: r.get(k, "") for k in keys})
                else:
                    with p.open("w", encoding="utf-8") as outfh:
                        json.dump(report_rows, outfh, ensure_ascii=False, indent=2)

            self.message_user(
                request,
                f"Assigned {assigned} users to group '{group}' (dry-run={dry_run})",
            )

            # Render a result page with report rows and optional download link
            media_url = getattr(settings, "MEDIA_URL", "")
            context = {
                "opts": self.model._meta,
                "report_rows": report_rows,
                "report_file": report_file,
                "report_format": report_format,
                "group": group,
                "dry_run": dry_run,
                "media_url": media_url,
            }
            return render(request, "admin/proje/owner_assign_result.html", context)

        # Otherwise render confirmation page
        context = {
            "owners": queryset,
            "group_form": self.GroupAssignActionForm(),
            "opts": self.model._meta,
            "action": "assign_group_to_owner_users",
        }
        return render(request, "admin/proje/owner_assign_confirm.html", context)


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
