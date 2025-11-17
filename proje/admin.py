import csv
import json
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.utils.html import format_html

from proje.models import Agreement, Document, Owner, Ownership, Project, Unit

from .admin_helpers import AdminBootstrapMixin
from .utils import generate_report_path


@admin.register(Project)
class ProjectAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    list_display = ("code", "name", "status", "manager")
    search_fields = ("code", "name", "location")
    list_filter = ("status", "type")


@admin.register(Owner)
class OwnerAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    list_display = ("first_name", "last_name", "tc_no", "phone")
    search_fields = ("first_name", "last_name", "tc_no")
    actions = ["assign_group_to_owner_users"]

    # Provide an action form to pick a group
    class GroupAssignActionForm(forms.Form):
        group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
        # Admin expects an 'action' field to exist; provide an empty ChoiceField
        action = forms.ChoiceField(choices=(), required=False)
        upload_s3 = forms.BooleanField(required=False, initial=False)
        s3_bucket = forms.CharField(required=False)
        s3_public = forms.BooleanField(required=False, initial=False)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # add consistent classes to widgets
            for name, field in self.fields.items():
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
            group_pk = request.POST.get("group")
            dry_run = request.POST.get("dry_run") == "on"
            report_file = request.POST.get("report_file") or ""
            report_format = request.POST.get("report_format") or "csv"
            upload_s3 = request.POST.get("upload_s3") == "on"
            s3_bucket = request.POST.get("s3_bucket") or None
            s3_public = request.POST.get("s3_public") == "on"

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

            # If admin didn't provide a path, auto-generate one using admin username
            if not report_file and report_rows:
                report_file = generate_report_path(
                    prefix="reports/owners_assign",
                    ext=report_format,
                    label=getattr(request.user, "username", None),
                )

            # write report if requested
            if report_file:
                # If report_file is absolute, write there; otherwise write under MEDIA_ROOT
                target_path = Path(report_file)
                if not target_path.is_absolute():
                    media_root = getattr(settings, "MEDIA_ROOT", None)
                    if media_root:
                        target_path = Path(media_root) / report_file
                    else:
                        target_path = Path(report_file)

                target_path.parent.mkdir(parents=True, exist_ok=True)
                if report_format == "csv":
                    keys = ["ident", "user", "group", "status"]
                    with target_path.open("w", newline="", encoding="utf-8") as outfh:
                        writer = csv.DictWriter(outfh, fieldnames=keys)
                        writer.writeheader()
                        for r in report_rows:
                            writer.writerow({k: r.get(k, "") for k in keys})
                else:
                    with target_path.open("w", encoding="utf-8") as outfh:
                        json.dump(report_rows, outfh, ensure_ascii=False, indent=2)

            # Optionally upload to S3
            report_s3_url = None
            if report_file and upload_s3:
                try:
                    from .utils import upload_file_to_s3

                    bucket = s3_bucket or getattr(settings, "REPORTS_S3_BUCKET", None)
                    res = upload_file_to_s3(
                        target_path, bucket=bucket, public=s3_public
                    )
                    report_s3_url = res.get("url")
                except Exception:
                    report_s3_url = None

            # prepare download URL if file is under MEDIA_ROOT
            report_file_url = None
            media_root = getattr(settings, "MEDIA_ROOT", None)
            if report_file and media_root:
                try:
                    relpath = Path(target_path).relative_to(media_root)
                    # Use admin-facing download view
                    from django.urls import reverse

                    report_file_url = reverse(
                        "proje:report_download", args=[str(relpath)]
                    )
                except Exception:
                    report_file_url = None

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
                "report_file_url": report_file_url,
                "report_s3_url": report_s3_url,
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
class UnitAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    list_display = ("project", "ada", "parsel", "type", "agreement_status")
    list_filter = ("type", "agreement_status")
    search_fields = ("ada", "parsel", "address")


class DocumentInline(AdminBootstrapMixin, admin.TabularInline):
    model = Document
    extra = 0
    # allow editing the file directly in the inline and show a change link
    fields = ("file", "label", "file_link", "uploaded_by", "uploaded_at")
    readonly_fields = ("file_link", "uploaded_by", "uploaded_at")
    show_change_link = True

    def file_link(self, obj):
        if not obj or not obj.file:
            return "-"
        url = getattr(obj.file, "url", None)
        name = obj.label or obj.file.name.split("/")[-1]
        # try to get file size and uploaded_by for metadata
        size = None
        uploader = None
        try:
            size = obj.file.size
        except Exception:
            size = None
        try:
            if getattr(obj.uploaded_by, "get_full_name", None):
                uploader = obj.uploaded_by.get_full_name()
            else:
                uploader = getattr(obj.uploaded_by, "username", None)
        except Exception:
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
    list_display = ("unit", "owner", "share_percent", "status")


@admin.register(Agreement)
class AgreementAdmin(AdminBootstrapMixin, admin.ModelAdmin):
    list_display = ("unit", "date", "status", "staff")


@admin.register(Document)
class DocumentAdmin(AdminBootstrapMixin, admin.ModelAdmin):
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
        if not obj or not obj.file:
            return "-"
        url = getattr(obj.file, "url", None)
        name = obj.label or obj.file.name.split("/")[-1]
        size = None
        uploader = None
        try:
            size = obj.file.size
        except Exception:
            size = None
        try:
            if getattr(obj.uploaded_by, "get_full_name", None):
                uploader = obj.uploaded_by.get_full_name()
            else:
                uploader = getattr(obj.uploaded_by, "username", None)
        except Exception:
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
                except Exception:
                    size = None
                try:
                    if getattr(obj.uploaded_by, "get_full_name", None):
                        uploader = obj.uploaded_by.get_full_name()
                    else:
                        uploader = getattr(obj.uploaded_by, "username", None)
                except Exception:
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
        css = {
            "all": (
                "proje/admin/document_preview.css",
                "proje/admin/admin_overrides.css",
            )
        }
        js = ("proje/admin/document_preview.js",)

    class DocumentBulkUploadForm(forms.ModelForm):
        # We handle the files upload via request.FILES.getlist('files') in add_view,
        # to avoid widget limitations. Labels are provided as textarea lines.
        labels = forms.CharField(
            widget=forms.Textarea,
            required=False,
            help_text="Her satıra bir etiket girin; dosyalarla sırayla eşlenecektir (örnek: sözleşme).",
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
            for name, field in self.fields.items():
                widget = field.widget
                css = widget.attrs.get("class", "")
                classes = (css + " form-control").strip()
                widget.attrs["class"] = classes

    def add_view(self, request, form_url="", extra_context=None):
        """Custom add view to support multiple file uploads with optional labels."""
        if request.method == "POST":
            form = self.DocumentBulkUploadForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist("files")
                labels_raw = form.cleaned_data.get("labels") or ""
                labels = [ln.strip() for ln in labels_raw.splitlines() if ln.strip()]
                project = form.cleaned_data.get("project")
                unit = form.cleaned_data.get("unit")
                uploaded_by = form.cleaned_data.get("uploaded_by") or request.user

                created = []
                for idx, f in enumerate(files):
                    label = labels[idx] if idx < len(labels) else ""
                    doc = Document.objects.create(
                        project=project,
                        unit=unit,
                        file=f,
                        label=label,
                        uploaded_by=uploaded_by,
                    )
                    created.append(doc)

                # After creation redirect to unit change page if unit provided, else to document changelist
                if unit:
                    from django.urls import reverse

                    return_url = reverse("admin:proje_unit_change", args=[unit.pk])
                else:
                    from django.urls import reverse

                    return_url = reverse("admin:proje_document_changelist")
                from django.shortcuts import redirect

                self.message_user(request, f"Yüklendi: {len(created)} dosya")
                return redirect(return_url)
        else:
            form = self.DocumentBulkUploadForm()

        # Render custom template using the form (falls back to admin add template fields)
        context = dict(
            self.admin_site.each_context(request),
            title="Proje Dosyası Ekle (Çoklu)",
            form=form,
            opts=self.model._meta,
        )
        from django.template.response import TemplateResponse

        return TemplateResponse(request, "admin/proje/document_add_bulk.html", context)
