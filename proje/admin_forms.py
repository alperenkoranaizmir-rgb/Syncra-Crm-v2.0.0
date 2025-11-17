"""Reusable admin forms for the `proje` app.

This module contains forms extracted from `proje.admin` so they can be
reused and unit-tested more easily.
"""

from django import forms
from django.contrib.auth.models import Group

from proje.models import Document


class GroupAssignActionForm(forms.Form):
    """Action form used by `OwnerAdmin.assign_group_to_owner_users`.

    Allows picking a `Group`, toggling S3 upload and providing an optional
    report file path.
    """

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
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
