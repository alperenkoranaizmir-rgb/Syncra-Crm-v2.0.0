"""Management command to create default groups, departments and titles.

This command is idempotent and safe to run repeatedly. It will:

- create the configured groups, departments and titles if missing
- assign sensible permission sets for each group using the project's
  content types and Django's Permission model

The permission mapping is conservative: missing content types or
permissions are skipped rather than causing an error, so the command
works in partial/test environments.
"""

from typing import Dict, Iterable, List

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from accounts.models import Department, Title


DEFAULT_GROUPS = [
    "KENTSEL DÖNÜŞÜM UZMANI",
    "PROJE YÖNETİCİSİ",
    "ADMİN",
    "MUHASEBE",
    "İNSAN KAYNAKLARI",
    "SATINALMA",
    "HUKUK",
    "BİLGİ İŞLEM",
    "SEKRETERYA",
    "HİZMETLİ",
    "ŞÖFÖR",
    "YÜKLENİCİ FİRMA",
    "İŞ GÜVENLİĞİ UZMANI",
    "SAĞLIK PERSONELİ",
    "TAŞERON FİRMA",
    "MİMARİ",
    "YÖNETİCİ",
]

DEFAULT_DEPARTMENTS = DEFAULT_GROUPS.copy()
DEFAULT_TITLES = [
    "Uzman",
    "Proje Yöneticisi",
    "Muhasebe Uzmanı",
    "İK Uzmanı",
    "Satınalma Uzmanı",
    "Hukuk Danışmanı",
]


# Permission assignment strategy per group. Values:
# - "all": grant all permissions
# - {"app": "app_label"}: grant all permissions for an app
# - {"app_perms": ("add","change") , "app": "app_label"}: grant add/change on app models
# - {"auth_user_manage": True}: grant add/change/view on auth.User and auth.Group
# - "view_proje": grant view_* permissions for `proje` app models
PERMISSION_MAP: Dict[str, object] = {
    "YÖNETİCİ": "all",
    "ADMİN": "all",
    "PROJE YÖNETİCİSİ": {"app": "proje"},
    "KENTSEL DÖNÜŞÜM UZMANI": {"app_perms": ("add", "change"), "app": "proje"},
    "MUHASEBE": {"app_perms": ("view", "change"), "app": "proje"},
    "İNSAN KAYNAKLARI": {"auth_user_manage": True},
    "SATINALMA": {"app_perms": ("view", "add", "change"), "app": "proje"},
    "HUKUK": {"app_perms": ("view", "change"), "app": "proje"},
    "BİLGİ İŞLEM": {"app_perms": ("view", "change"), "app": "auth"},
    "SEKRETERYA": {"app_perms": ("view", "add"), "app": "proje"},
    "HİZMETLİ": "view_proje",
    "ŞÖFÖR": "view_proje",
    "YÜKLENİCİ FİRMA": "view_proje",
    "İŞ GÜVENLİĞİ UZMANI": {"app_perms": ("view", "add"), "app": "proje"},
    "SAĞLIK PERSONELİ": {"app_perms": ("view", "add"), "app": "proje"},
    "TAŞERON FİRMA": "view_proje",
    "MİMARİ": {"app_perms": ("view", "change"), "app": "proje"},
}


def _perms_for_app(app_label: str) -> Iterable[Permission]:
    """Yield all Permission objects for a given app label."""

    return Permission.objects.filter(content_type__app_label=app_label)


def _perms_for_app_and_actions(app_label: str, actions: Iterable[str]) -> Iterable[Permission]:
    """Yield permissions for app models matching the given action prefixes.

    e.g. actions=("add","change") will match codenames starting with
    "add_" or "change_" for the given app_label.
    """

    qs = Permission.objects.filter(content_type__app_label=app_label)
    prefixes = tuple(f"{a}_" for a in actions)
    return qs.filter(codename__startswith=prefixes)


class Command(BaseCommand):
    """Create default groups, departments, titles and set permissions."""

    help = "Create default groups, departments, titles and set sensible permissions"

    def handle(self, *args, **options):
        created: List[str] = []

        # Create groups and basic domain objects
        for g in DEFAULT_GROUPS:
            grp, created_flag = Group.objects.get_or_create(name=g)
            if created_flag:
                created.append(f"group:{g}")

        for d in DEFAULT_DEPARTMENTS:
            _, created_flag = Department.objects.get_or_create(name=d)
            if created_flag:
                created.append(f"department:{d}")

        for t in DEFAULT_TITLES:
            _, created_flag = Title.objects.get_or_create(name=t)
            if created_flag:
                created.append(f"title:{t}")

        # Apply permission mapping
        for group_name, rule in PERMISSION_MAP.items():
            try:
                grp = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                # If group is missing (shouldn't be), skip silently
                continue

            if rule == "all":
                perms = Permission.objects.all()
                grp.permissions.set(perms)
                created.append(f"perms:{group_name}=all")
                continue

            if isinstance(rule, dict):
                if rule.get("auth_user_manage"):
                    # Manage users and groups (add/change/view)
                    perms = Permission.objects.filter(
                        content_type__app_label="auth",
                        codename__in=("add_user", "change_user", "view_user", "add_group", "change_group", "view_group"),
                    )
                    grp.permissions.add(*perms)
                    created.append(f"perms:{group_name}=auth_user_manage")
                    continue

                app = rule.get("app")
                if app and rule.get("app_perms"):
                    perms = _perms_for_app_and_actions(app, rule["app_perms"])
                    grp.permissions.add(*perms)
                    created.append(f"perms:{group_name}={app}:{','.join(rule['app_perms'])}")
                    continue

                if app and not rule.get("app_perms"):
                    perms = _perms_for_app(app)
                    grp.permissions.add(*perms)
                    created.append(f"perms:{group_name}=app:{app}")
                    continue

            if rule == "view_proje":
                # conservative: only grant view_* permissions for `proje` app
                perms = Permission.objects.filter(content_type__app_label="proje", codename__startswith="view_")
                grp.permissions.add(*perms)
                created.append(f"perms:{group_name}=view_proje")

        # Ensure 'YÖNETİCİ' behaves like a superuser (all permissions)
        try:
            admin_grp = Group.objects.get(name="YÖNETİCİ")
            admin_grp.permissions.set(Permission.objects.all())
            created.append("perms:YÖNETİCİ=all")
        except Group.DoesNotExist:
            pass

        # Summary output
        if created:
            self.stdout.write("Created/updated: \n" + "\n".join(created))
        else:
            self.stdout.write("No changes made. All groups, departments and titles already exist")
