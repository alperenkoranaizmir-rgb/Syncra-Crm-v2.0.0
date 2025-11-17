"""Management command to create default groups, departments and titles.

This command is safe to run multiple times; it will create missing
groups/departments/titles and assign permissions to the 'YÖNETİCİ' group.
"""
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


class Command(BaseCommand):
    """Create default groups, departments and titles."""

    help = "Create default groups, departments and titles"

    def handle(self, *args, **options):
        created = []
        for g in DEFAULT_GROUPS:
            _, created_flag = Group.objects.get_or_create(name=g)
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

        # Give 'YÖNETİCİ' group all permissions (like superuser)
        try:
            admin_grp = Group.objects.get(name="YÖNETİCİ")
            perms = Permission.objects.all()
            admin_grp.permissions.set(perms)
            admin_grp.save()
            created.append("perms:YÖNETİCİ=all")
        except Group.DoesNotExist:
            pass

        self.stdout.write(f"Created: {', '.join(created)}")
