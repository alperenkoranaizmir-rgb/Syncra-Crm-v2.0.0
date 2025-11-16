from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Assign a user to a project-related group. Usage: "
        "python manage.py proje_assign_group --username <username> --group 'Proje Yöneticisi'"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", type=str, help="Username (or email) of the user"
        )
        parser.add_argument(
            "--group", type=str, help="Group name to assign (e.g. 'Proje Yöneticisi')"
        )
        parser.add_argument(
            "--file",
            type=str,
            help="CSV file path for bulk assign. Columns: username or email; optional column 'group' or use --group",
        )
        parser.add_argument(
            "--users",
            type=str,
            help="Comma-separated list of usernames or emails to assign to --group",
        )

    def handle(self, *args, **options):
        username = options.get("username")
        group_name = options.get("group")

        file_path = options.get("file")
        users_arg = options.get("users")

        # Determine mode: single, bulk-by-list, or bulk-by-file
        if file_path:
            # bulk via CSV file; group may be provided as global or per-row
            import csv

            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group

            User = get_user_model()

            group_global = group_name
            assigned = 0
            with open(file_path, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                # Accept files with header 'username' or 'email' and optional 'group'
                for row in reader:
                    ident = row.get("username") or row.get("email")
                    if not ident:
                        continue
                    gname = row.get("group") or group_global
                    if not gname:
                        self.stdout.write(f"Skipping {ident}: no group provided\n")
                        continue
                    try:
                        user = User.objects.get(username=ident)
                    except User.DoesNotExist:
                        try:
                            user = User.objects.get(email=ident)
                        except User.DoesNotExist:
                            self.stdout.write(f"User '{ident}' not found; skipping\n")
                            continue
                    group, _ = Group.objects.get_or_create(name=gname)
                    group.user_set.add(user)
                    assigned += 1
            self.stdout.write(f"Assigned {assigned} users from {file_path}\n")
            return

        if users_arg:
            # comma-separated list
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group

            User = get_user_model()
            if not group_name:
                raise CommandError("--group is required when using --users")
            usernames = [u.strip() for u in users_arg.split(",") if u.strip()]
            assigned = 0
            for ident in usernames:
                try:
                    user = User.objects.get(username=ident)
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email=ident)
                    except User.DoesNotExist:
                        self.stdout.write(f"User '{ident}' not found; skipping\n")
                        continue
                group, _ = Group.objects.get_or_create(name=group_name)
                group.user_set.add(user)
                assigned += 1
            self.stdout.write(f"Assigned {assigned} users from list\n")
            return

        # fall back to single user mode
        if not username or not group_name:
            raise CommandError(
                "Either --username and --group, or --file, or --users and --group must be provided"
            )

        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Group

        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            # try email as fallback
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                raise CommandError(f"User '{username}' not found") from exc

        group, _ = Group.objects.get_or_create(name=group_name)
        group.user_set.add(user)
        # Use plain write to avoid type issues in static analysis
        self.stdout.write(f"Added user {user} to group '{group_name}'\n")
