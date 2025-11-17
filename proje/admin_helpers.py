"""Admin helper utilities used by `proje.admin`.

This module contains small helpers to keep admin ModelAdmin classes concise,
for example widget class injection and report/upload helpers used by
bulk actions.
"""

from django import forms


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
    from pathlib import Path
    from django.conf import settings

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
