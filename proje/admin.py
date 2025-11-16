from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

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
    actions = ["assign_group_to_owner_users"]

    # Provide an action form to pick a group
    class GroupAssignActionForm(forms.Form):
        group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    action_form = GroupAssignActionForm

    @admin.action(description="Assign selected owners (by email) to a Group")
    def assign_group_to_owner_users(self, request, queryset):
        """Admin action: assign selected owners' emails (if matching a User) to chosen group."""
        group = None
        # action form provides cleaned_data in request.POST via 'action' form; fallback to first group
        group_pk = request.POST.get("group")
        if group_pk:
            group = Group.objects.filter(pk=group_pk).first()

        if not group:
            # fallback: use first group (not ideal) and notify
            group = Group.objects.first()
            if not group:
                self.message_user(request, "No groups defined; nothing to do")
                return
            self.message_user(
                request, f"No group selected; using '{group}' as fallback"
            )

        User = get_user_model()
        assigned = 0
        for owner in queryset:
            if owner.email:
                try:
                    user = User.objects.get(email__iexact=owner.email)
                except User.DoesNotExist:
                    continue
                group.user_set.add(user)
                assigned += 1

        self.message_user(request, f"Assigned {assigned} users to group '{group}'")


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
