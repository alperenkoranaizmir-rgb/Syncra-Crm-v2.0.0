"""Forms for accounts app: user profile create/update and admin forms."""
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileForm(forms.ModelForm):
    """Form for editing Profile information (IK kullanımı)."""

    class Meta:
        model = Profile
        fields = (
            "gms",
            "phone_fixed",
            "birth_date",
            "tc_no",
            "address",
            "photo",
            "department",
            "title",
            "job_start",
            "job_end",
            "is_active_employee",
        )


class UserAdminForm(forms.ModelForm):
    """Simple user admin form to edit basic User fields via accounts."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_active")
