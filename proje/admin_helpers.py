"""Admin helper utilities used by `proje.admin`.

This module contains small helpers to keep admin ModelAdmin classes concise,
for example widget class injection and report/upload helpers used by
bulk actions.
"""

from pathlib import Path
from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from proje.models import Document


class AdminBootstrapMixin:
    """Mixin to add Bootstrap/AdminLTE classes to ModelAdmin forms and inlines.

    Use by inheriting before `admin.ModelAdmin` or `admin.TabularInline`.
    """

    def _add_bootstrap(self, form):
        """Apply Bootstrap/AdminLTE classes to form widgets in `form`.

        This is a best-effort helper that modifies `widget.attrs['class']`
        to include framework-specific classes and silently ignores widgets
        that do not support attrs.
        """
        for field in getattr(form, "base_fields", {}).values():
            widget = field.widget
            try:
                # File inputs should use form-control-file
                if isinstance(widget, forms.FileInput):
                    css = widget.attrs.get("class", "")
                    widget.attrs["class"] = (css + " form-control-file").strip()
                # Checkbox inputs get form-check-input
                elif isinstance(widget, forms.CheckboxInput):
                    css = widget.attrs.get("class", "")
                    widget.attrs["class"] = (css + " form-check-input").strip()
                else:
                    css = widget.attrs.get("class", "")
                    widget.attrs["class"] = (css + " form-control").strip()
            except (AttributeError, TypeError):
                # best-effort: if widget lacks attrs or is unexpected, don't break admin
                pass

    def get_form(self, request, obj=None, **kwargs):
        """Return the admin form class and apply bootstrap classes to widgets.

        Wraps `super().get_form` to ensure widget classes are adjusted for
        AdminLTE/Bootstrap styling before the form is used in the admin UI.
        """
        form = super().get_form(request, obj, **kwargs)
        # apply classes to form fields
        try:
            self._add_bootstrap(form)
        except (AttributeError, TypeError):
            # best-effort application of classes; don't fail admin rendering
            pass
        return form


def save_report_rows(report_rows, report_file, report_format="csv"):
    """Write `report_rows` to `report_file` (absolute or relative).

    If `report_file` is relative, it will be placed under `settings.MEDIA_ROOT`
    when available. Returns a `pathlib.Path` pointing to the written file.
    """
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
            import csv

            writer = csv.DictWriter(outfh, fieldnames=keys)
            writer.writeheader()
            for r in report_rows:
                writer.writerow({k: r.get(k, "") for k in keys})
    else:
        with target_path.open("w", encoding="utf-8") as outfh:
            import json

            json.dump(report_rows, outfh, ensure_ascii=False, indent=2)

    return target_path


def upload_report_to_s3(target_path, bucket=None, public=False):
    """Attempt to upload `target_path` to S3 and return a public URL or None.

    This function wraps the project `upload_file_to_s3` helper when available
    and returns `None` on error.
    """
    try:
        from .utils import upload_file_to_s3

        res = upload_file_to_s3(target_path, bucket=bucket, public=public)
        return res.get("url")
    except Exception:  # pragma: no cover - best-effort
        # Best-effort upload; do not propagate exceptions to admin UI
        # pylint: disable=broad-except
        return None


def build_owner_assign_report(owners_queryset, group, dry_run=False):
    """Build report rows for owner->user assignment and perform assignment.

    Given an iterable of `Owner` instances and a `Group` instance, return a
    tuple `(report_rows, assigned_count)`. If `dry_run` is False, users will
    be added to the group's `user_set`; when True, no database changes are
    performed and the helper only reports what would happen.
    """
    # Helper split into smaller functions to reduce local variable pressure
    # and improve readability.

    def _owner_ident(o):
        return (o.email or "").strip()

    def _find_user_by_ident(ident):
        return get_user_model().objects.filter(email__iexact=ident).first()

    def _row(ident, user_obj, grp, status):
        return {
            "ident": ident,
            "user": str(user_obj) if user_obj is not None else "",
            "group": str(grp) if grp is not None else "",
            "status": status,
        }

    report_rows = []
    assigned = 0
    for owner in owners_queryset:
        ident = _owner_ident(owner)
        if not ident:
            report_rows.append(_row(str(owner), None, None, "no_email"))
            continue

        user = _find_user_by_ident(ident)
        if not user:
            report_rows.append(_row(ident, None, None, "not_found"))
            continue

        if dry_run:
            report_rows.append(_row(ident, user, group, "would_assign"))
            continue

        # perform the assignment and record it
        group.user_set.add(user)
        assigned += 1
        report_rows.append(_row(ident, user, group, "assigned"))

    return report_rows, assigned


def prepare_owner_report(
    report_rows,
    report_file,
    report_format,
    request_user,
    upload_options=None,
):
    """Prepare, write and optionally upload an owner assignment report.

    `upload_options` is an optional dict with keys `upload_s3`, `s3_bucket`
    and `s3_public` to control S3 upload behavior.

    Returns `(target_path, report_file, report_file_url, report_s3_url)`.
    """
    upload_options = upload_options or {}
    upload_s3 = bool(upload_options.get("upload_s3"))
    s3_bucket = upload_options.get("s3_bucket")
    s3_public = bool(upload_options.get("s3_public"))

    target_path = None
    report_file_url = None
    report_s3_url = None

    # Auto-generate filename when missing. Include username when available.
    if not report_file and report_rows:
        from .utils import generate_report_path

        report_file = generate_report_path(
            prefix="reports/owners_assign",
            ext=report_format,
            label=getattr(request_user, "username", None),
        )

    if report_file:
        target_path = save_report_rows(report_rows, report_file, report_format)

        if upload_s3:
            bucket = s3_bucket or getattr(settings, "REPORTS_S3_BUCKET", None)
            report_s3_url = upload_report_to_s3(
                target_path,
                bucket=bucket,
                public=s3_public,
            )

        media_root = getattr(settings, "MEDIA_ROOT", None)
        if target_path and media_root:
            try:
                relpath = Path(target_path).relative_to(media_root)
                report_file_url = reverse("proje:report_download", args=[str(relpath)])
            except Exception:  # pylint: disable=broad-except
                report_file_url = None

    return target_path, report_file, report_file_url, report_s3_url


def create_documents_from_files(files, labels, project, unit, uploaded_by):
    """Create Document instances from uploaded `files` and parallel `labels` list.

    Returns a list of created `Document` instances.
    """
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
    return created


def build_document_return_url(unit):
    """Return admin redirect URL after bulk document upload.

    If `unit` is provided, returns the unit change URL, otherwise the
    document changelist URL.
    """
    if unit:
        return reverse("admin:proje_unit_change", args=[unit.pk])
    return reverse("admin:proje_document_changelist")


def parse_owner_assign_post(post_data):
    """Parse POST-like mapping for owner assign action and return params dict.

    Accepts a mapping with `.get()` (e.g. `request.POST`) and returns a dict with
    keys: ``group_pk``, ``dry_run``, ``report_file``, ``report_format``,
    ``upload_s3``, ``s3_bucket``, ``s3_public``.
    """
    group_pk = post_data.get("group")
    dry_run = post_data.get("dry_run") == "on"
    report_file = post_data.get("report_file") or ""
    report_format = post_data.get("report_format") or "csv"
    upload_s3 = post_data.get("upload_s3") == "on"
    s3_bucket = post_data.get("s3_bucket") or None
    s3_public = post_data.get("s3_public") == "on"

    return {
        "group_pk": group_pk,
        "dry_run": dry_run,
        "report_file": report_file,
        "report_format": report_format,
        "upload_s3": upload_s3,
        "s3_bucket": s3_bucket,
        "s3_public": s3_public,
    }


def build_owner_assign_context(model_meta, report_info, group, dry_run, media_url):
    """Return context dict for the owner-assign result template.

    `report_info` is a dict containing keys: ``report_file``, ``report_file_url``,
    ``report_s3_url`` and ``report_format``. `model_meta` is typically
    `self.model._meta` from the calling ModelAdmin.
    """
    return {
        "opts": model_meta,
        "report_rows": report_info.get("report_rows"),
        "report_file": report_info.get("report_file"),
        "report_file_url": report_info.get("report_file_url"),
        "report_s3_url": report_info.get("report_s3_url"),
        "report_format": report_info.get("report_format"),
        "group": group,
        "dry_run": dry_run,
        "media_url": media_url,
    }
