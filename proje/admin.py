"""Django admin customizations for the `proje` app.

Provides ModelAdmin classes and helper add views used in the admin site.
This module centralizes admin UI tweaks (inlines, bulk upload, custom actions)
and includes styling hooks for AdminLTE/Bootstrap integration.
"""

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib import messages

from django.contrib.auth.models import Group
from django.shortcuts import render
from django.utils.html import format_html
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from proje.models import Agreement, Document, Owner, Ownership, Project, Unit

from .admin_helpers import (
    AdminBootstrapMixin,
    perform_owner_assignment,
    process_bulk_document_upload,
    create_documents_from_files,
    build_document_return_url,
)


@admin.register(Project)
class ProjectAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    """Admin for `Project` model: list/filters and basic search configuration."""
    list_display = ("code", "name", "status", "manager")
    search_fields = ("code", "name", "location")
    list_filter = ("status", "type")


@admin.register(Owner)
class OwnerAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    """Admin for `Owner` model including bulk group-assign actions."""
    list_display = ("first_name", "last_name", "tc_no", "phone")
    search_fields = ("first_name", "last_name", "tc_no")
    actions = ["assign_group_to_owner_users"]

    # Provide an action form to pick a group
    class GroupAssignActionForm(forms.Form):
        """Action form used by the OwnerAdmin.assign_group_to_owner_users action.

        Allows picking a group, toggling S3 upload and providing an optional
        report file path.
        """
        group = forms.ModelChoiceField(
            queryset=Group.objects.all(),
            required=True,
        )
        # Admin expects an 'action' field to exist; provide an empty ChoiceField
        action = forms.ChoiceField(choices=(), required=False)
        upload_s3 = forms.BooleanField(required=False, initial=False)
        s3_bucket = forms.CharField(required=False)
        s3_public = forms.BooleanField(required=False, initial=False)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # add consistent classes to widgets
            for _, field in self.fields.items():
                widget = field.widget
                css = widget.attrs.get("class", "")
                widget.attrs["class"] = (css + " form-control").strip()

    action_form = GroupAssignActionForm

    @admin.action(description="Assign selected owners (by email) to a Group")
    def assign_group_to_owner_users(self, request, queryset):
        """Admin action with confirmation form. Shows a confirmation page where admin
        can choose the Group, toggle dry-run, and optionally provide a report file path.
        On confirmation the selected owners are matched by `email` to Users and assigned.
        """
        # If this is the confirmation POST, perform assignment
        if request.method == "POST" and request.POST.get("confirm"):
            # Delegate POST processing to helper to reduce ModelAdmin complexity
            result = perform_owner_assignment(request, queryset, self)
            if result is None:
                return None
            template_name, context = result
            return render(request, template_name, context)

        # Otherwise render confirmation page
        context = {
            "owners": queryset,
            "group_form": self.GroupAssignActionForm(),
            "opts": self.model._meta,  # pylint: disable=protected-access
            "action": "assign_group_to_owner_users",
        }
        return render(request, "admin/proje/owner_assign_confirm.html", context)


@admin.register(Unit)
class UnitAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    """Admin for `Unit` model: list, filters and search configuration."""
    list_display = ("project", "ada", "parsel", "type", "agreement_status")
    list_filter = ("type", "agreement_status")
    search_fields = ("ada", "parsel", "address")


class DocumentInline(AdminBootstrapMixin, admin.TabularInline):
    """Inline admin for `Document` entries attached to a `Unit`.

    Shows a small file thumbnail/link and basic metadata in the inline table.
    """
    extra = 0
    model = Document
    # allow editing the file directly in the inline and show a change link
    fields = ("file", "label", "file_link", "uploaded_by", "uploaded_at")
    readonly_fields = ("file_link", "uploaded_by", "uploaded_at")
    show_change_link = True

    def file_link(self, obj):
        """Return an HTML link or filename for the inline document preview."""
        if not obj or not obj.file:
            return "-"
        url = getattr(obj.file, "url", None)
        name = obj.label or obj.file.name.split("/")[-1]
        # try to get file size and uploaded_by for metadata
        size = None
        uploader = None
        try:
            size = obj.file.size
        except (AttributeError, OSError):
            size = None
        try:
            if getattr(obj.uploaded_by, "get_full_name", None):
                uploader = obj.uploaded_by.get_full_name()
            else:
                uploader = getattr(obj.uploaded_by, "username", None)
        except AttributeError:
            uploader = None
        # Render a clickable thumbnail link when possible, including metadata attrs
        if url:
            tpl = (
                '<a href="{}" class="doc-thumb-link" data-full="{}" '
                'data-size="{}" data-uploader="{}" target="_blank">{}</a>'
            )
            return format_html(tpl, url, url, size or "", uploader or "", name)
        return name

    file_link.short_description = "Dosya"  # type: ignore[attr-defined]

    class Media:
        """Media assets (CSS/JS) required by the Document inline preview UI."""
        css = {
            "all": (
                "proje/admin/document_preview.css",
                "proje/admin/admin_overrides.css",
            )
        }
        js = ("proje/admin/document_preview.js",)


# attach inline to UnitAdmin
UnitAdmin.inlines = [DocumentInline]


@admin.register(Ownership)
class OwnershipAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    """Admin for `Ownership` model (unit-owner relationship)."""
    list_display = ("unit", "owner", "share_percent", "status")


@admin.register(Agreement)
class AgreementAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    """Admin for `Agreement` model (unit agreements)."""
    list_display = ("unit", "date", "status", "staff")


@admin.register(Document)
class DocumentAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    """Admin for `Document` model with preview and bulk upload support."""
    list_display = (
        "label",
        "file_link",
        "project",
        "unit",
        "uploaded_by",
        "uploaded_at",
    )
    readonly_fields = ("uploaded_at", "preview")
    search_fields = ("label", "file__icontains")
    fields = (
        "label",
        "preview",
        "file",
        "project",
        "unit",
        "uploaded_by",
        "uploaded_at",
    )

    def file_link(self, obj):
        """Return an HTML link or filename for the document preview in list view."""
        if not obj or not obj.file:
            return "-"
        url = getattr(obj.file, "url", None)
        name = obj.label or obj.file.name.split("/")[-1]
        size = None
        uploader = None
        try:
            size = obj.file.size
        except (AttributeError, OSError):
            size = None
        try:
            if getattr(obj.uploaded_by, "get_full_name", None):
                uploader = obj.uploaded_by.get_full_name()
            else:
                uploader = getattr(obj.uploaded_by, "username", None)
        except AttributeError:
            uploader = None
        if url:
            tpl = (
                '<a href="{}" class="doc-thumb-link" data-full="{}" '
                'data-size="{}" data-uploader="{}" target="_blank">{}</a>'
            )
            return format_html(tpl, url, url, size or "", uploader or "", name)
        return name

    file_link.short_description = "Dosya"  # type: ignore[attr-defined]

    def preview(self, obj):
        """Show an image thumbnail for image files, or a file icon/name otherwise."""
        if not obj or not obj.file:
            return "-"
        url = getattr(obj.file, "url", None)
        # crude image detection by extension
        if url:
            fname = str(obj.file.name).lower()
            if fname.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                # Include metadata attrs and return a thumbnail link (opens lightbox)
                size = None
                uploader = None
                try:
                    size = obj.file.size
                except (AttributeError, OSError):
                    size = None
                try:
                    if getattr(obj.uploaded_by, "get_full_name", None):
                        uploader = obj.uploaded_by.get_full_name()
                    else:
                        uploader = getattr(obj.uploaded_by, "username", None)
                except AttributeError:
                    uploader = None
                tpl = (
                    '<a href="{}" class="doc-thumb-link" data-full="{}" '
                    'data-size="{}" data-uploader="{}"><img src="{}" class="doc-thumb"/></a>'
                )
                return format_html(tpl, url, url, size or "", uploader or "", url)
        # not an image -- show clickable name
        name = obj.label or obj.file.name.split("/")[-1]
        if url:
            return format_html('<a href="{}" target="_blank">{}</a>', url, name)
        return name

    preview.short_description = "Önizleme"  # type: ignore[attr-defined]

    class Media:
        """Media assets (CSS/JS) required by the Document admin preview UI."""
        css = {
            "all": (
                "proje/admin/document_preview.css",
                "proje/admin/admin_overrides.css",
            )
        }
        js = ("proje/admin/document_preview.js",)

    class DocumentBulkUploadForm(forms.ModelForm):
        """Form used by `DocumentAdmin.add_view` to accept multiple files.

        We handle the file list via `request.FILES.getlist('files')` in
        `add_view`; labels are provided as newline-separated textarea input.
        """
        labels = forms.CharField(
            widget=forms.Textarea,
            required=False,
            help_text=(
                "Her satıra bir etiket girin; dosyalarla sırayla eşlenecektir "
                "(örnek: sözleşme)."
            ),
        )

        class Meta:
            model = Document
            fields = (
                "project",
                "unit",
                "uploaded_by",
            )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Add Bootstrap / AdminLTE classes to widgets for consistent styling
            for _, field in self.fields.items():
                widget = field.widget
                css = widget.attrs.get("class", "")
                classes = (css + " form-control").strip()
                widget.attrs["class"] = classes

    def add_view(self, request, form_url="", extra_context=None):
        """Custom add view to support multiple file uploads with optional labels."""
        # Delegate bulk upload handling to helper for clarity and testability
        redirect_url, created_count_or_form = process_bulk_document_upload(
            request, self.DocumentBulkUploadForm, self
        )
        if redirect_url:
            return redirect(redirect_url)
        # created_count_or_form is actually the form when redirect_url is falsy
        form = created_count_or_form

        # Render custom template using the form (falls back to admin add template fields)
        context = dict(
            self.admin_site.each_context(request),
            title="Proje Dosyası Ekle (Çoklu)",
            form=form,
            opts=self.model._meta,  # pylint: disable=protected-access
        )

        return TemplateResponse(request, "admin/proje/document_add_bulk.html", context)
