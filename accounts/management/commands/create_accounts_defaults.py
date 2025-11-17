"""Management command to create default groups and departments."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import Department, Title
from django.contrib.auth import get_user_model

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
    help = "Create default groups, departments and titles"

    def handle(self, *args, **options):
        created = []
        for g in DEFAULT_GROUPS:
            grp, ok = Group.objects.get_or_create(name=g)
            if ok:
                created.append(f"group:{g}")
        for d in DEFAULT_DEPARTMENTS:
            dep, ok = Department.objects.get_or_create(name=d)
            if ok:
                created.append(f"department:{d}")
        for t in DEFAULT_TITLES:
            tit, ok = Title.objects.get_or_create(name=t)
            if ok:
                created.append(f"title:{t}")

        # Give 'YÖNETİCİ' group all permissions (like superuser)
        try:
            admin_grp = Group.objects.get(name="YÖNETİCİ")
            # assign all permissions
            perms = Permission.objects.all()
            admin_grp.permissions.set(perms)
            admin_grp.save()
            created.append("perms:YÖNETİCİ=all")
        except Group.DoesNotExist:
            pass

        self.stdout.write("Created: %s" % (", ".join(created)))
