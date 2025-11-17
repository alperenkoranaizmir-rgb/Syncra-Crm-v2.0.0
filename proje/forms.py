"""Forms for the `proje` application.

Contains ModelForm definitions used by views and the admin interface.
"""

from django import forms

from proje.models import Agreement, Document, Owner, Project, Unit


class ProjectForm(forms.ModelForm):
    """Form for creating and editing `Project` instances.

    Used by admin and public-facing views to validate project data.
    """
    class Meta:
        model = Project
        fields = [
            "name",
            "code",
            "location",
            "area_m2",
            "type",
            "est_delivery_date",
            "est_budget",
            "status",
            "start_date",
            "est_end_date",
            "manager",
            "staff",
            "unit_count",
        ]


class OwnerForm(forms.ModelForm):
    """Form for creating and editing `Owner` instances."""
    class Meta:
        model = Owner
        fields = "__all__"


class UnitForm(forms.ModelForm):
    """Form for creating and editing `Unit` instances linked to a `Project`."""
    class Meta:
        model = Unit
        fields = [
            "project",
            "ada",
            "parsel",
            "m2",
            "address",
            "door_outside",
            "door_inside",
            "type",
            "current_m2",
            "share_m2",
            "occupancy",
            "agreement_status",
        ]


class AgreementForm(forms.ModelForm):
    """Form used to record an `Agreement` for a `Unit`."""
    class Meta:
        model = Agreement
        fields = ["unit", "date", "staff", "note", "status", "owners"]


class DocumentForm(forms.ModelForm):
    """Form for uploading `Document` files related to projects/units."""
    class Meta:
        model = Document
        fields = ["project", "unit", "file"]
