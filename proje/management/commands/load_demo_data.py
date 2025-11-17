from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from proje.models import Document, Owner, Ownership, Project, Unit


class Command(BaseCommand):
    help = "Load demo data: users, groups, projects, owners, units and sample documents"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove previously created demo objects (by code prefix) before creating new ones",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        clear = options.get("clear")

        self.stdout.write("Loading demo data...")

        if clear:
            self._clear_demo()

        # create groups
        groups = ["Proje Yöneticisi", "TestGroup"]
        for g in groups:
            Group.objects.get_or_create(name=g)

        # create users
        admin, _ = User.objects.get_or_create(
            username="admin_demo",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        alice, _ = User.objects.get_or_create(
            username="alice_demo", defaults={"email": "alice@example.com"}
        )
        bob, _ = User.objects.get_or_create(
            username="bob_demo", defaults={"email": "bob@example.com"}
        )

        # set passwords if not set
        for u in (admin, alice, bob):
            if not u.has_usable_password():
                u.set_password("demo1234")
                u.save()

        # create projects
        p1, _ = Project.objects.get_or_create(
            code="DEMO001",
            defaults={
                "name": "Demo Proje 1",
                "location": "Izmir",
                "manager": alice,
                "status": "planlama",
            },
        )
        p1.staff.add(bob)

        Project.objects.get_or_create(
            code="DEMO002",
            defaults={
                "name": "Demo Proje 2",
                "location": "Ankara",
                "manager": bob,
                "status": "uzlasma",
            },
        )

        # create owners, units and ownerships
        owner1, _ = Owner.objects.get_or_create(
            project=p1,
            first_name="Mehmet",
            last_name="Yilmaz",
            defaults={"email": "mehmet@example.com"},
        )
        unit1, _ = Unit.objects.get_or_create(
            project=p1, ada="1", parsel="1", defaults={"m2": 85}
        )
        Ownership.objects.get_or_create(
            unit=unit1, owner=owner1, defaults={"share_percent": 100}
        )

        # create a sample document for p1
        media_root = Path(getattr(settings, "MEDIA_ROOT", "."))
        media_root.mkdir(parents=True, exist_ok=True)
        reports_dir = media_root / "proje_documents"
        reports_dir.mkdir(parents=True, exist_ok=True)

        sample_path = reports_dir / "demo_readme.txt"
        if not sample_path.exists():
            sample_path.write_text("Demo proje dosyası\n", encoding="utf-8")

        # attach Document instance
        if not Document.objects.filter(label="demo_readme").exists():
            doc = Document(project=p1, label="demo_readme", uploaded_by=alice)
            with open(sample_path, "rb") as fh:
                doc.file.save("demo_readme.txt", ContentFile(fh.read()), save=True)

        self.stdout.write(self.style.SUCCESS("Demo data loaded successfully."))

    def _clear_demo(self):
        # remove demo-created objects
        User = get_user_model()
        User.objects.filter(username__endswith="_demo").delete()
        Project.objects.filter(code__startswith="DEMO").delete()
        Document.objects.filter(label__in=("demo_readme",)).delete()
        Owner.objects.filter(email__endswith="@example.com").delete()
