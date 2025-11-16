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

    def handle(self, *args, **options):
        username = options.get("username")
        group_name = options.get("group")

        if not username or not group_name:
            raise CommandError("Both --username and --group are required")

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
