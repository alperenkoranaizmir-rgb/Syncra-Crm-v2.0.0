"""Admin registrations for accounts app (departments, titles, profiles)."""
from django.contrib import admin
from .models import Department, Title, Profile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Departman yönetimi (ekle/güncelle/sil)."""
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Ünvan yönetimi."""
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Kullanıcı profili yönetimi."""
    list_display = ("user", "department", "title", "is_active_employee")
    search_fields = ("user__username", "user__email", "tc_no")
    list_filter = ("department", "title", "is_active_employee")
    readonly_fields = ("record_date",)
    fieldsets = (
        (None, {"fields": ("user", "photo", "is_active_employee")} ),
        ("İletişim", {"fields": ("gms", "phone_fixed", "address")} ),
        ("Personel", {"fields": ("department", "title", "job_start", "job_end", "record_date")} ),
    )
