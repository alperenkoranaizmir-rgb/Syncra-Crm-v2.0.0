import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from proje.utils import generate_report_path


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
            "--dry-run",
            action="store_true",
            help="Show what would be assigned without making changes",
        )
        parser.add_argument(
            "--users",
            type=str,
            help="Comma-separated list of usernames or emails to assign to --group",
        )
        parser.add_argument(
            "--report-file",
            type=str,
            help="Write a report of the assignments to this file (CSV or JSON by --report-format)",
        )
        parser.add_argument(
            "--report-format",
            type=str,
            choices=("csv", "json"),
            default="csv",
            help="Report file format when --report-file is used (csv or json)",
        )
        parser.add_argument(
            "--upload-s3",
            action="store_true",
            help="Upload generated report to S3 (bucket must be provided via --s3-bucket or settings)",
        )
        parser.add_argument(
            "--s3-bucket",
            type=str,
            help="S3 bucket to upload the report to (overrides settings.REPORTS_S3_BUCKET)",
        )
        parser.add_argument(
            "--s3-key",
            type=str,
            help="S3 object key to use for the uploaded report (by default filename is used)",
        )
        parser.add_argument(
            "--s3-public",
            action="store_true",
            help="Make uploaded S3 object public and return a public URL instead of a presigned URL",
        )
        parser.add_argument(
            "--label",
            type=str,
            help="Optional label to include in auto-generated report filename (e.g. project code)",
        )

    def handle(self, *args, **options):
        username = options.get("username")
        group_name = options.get("group")

        file_path = options.get("file")
        users_arg = options.get("users")
        dry_run = options.get("dry_run")
        report_file = options.get("report_file")
        report_format = options.get("report_format")
        label = options.get("label")
        upload_s3 = options.get("upload_s3")
        s3_bucket = options.get("s3_bucket")
        s3_key = options.get("s3_key")
        s3_public = options.get("s3_public")

        # helper to resolve user by username or email
        def _find_user(User, ident: str):
            ident = (ident or "").strip()
            if not ident:
                return None
            try:
                return User.objects.get(username=ident)
            except User.DoesNotExist:
                try:
                    return User.objects.get(email=ident)
                except User.DoesNotExist:
                    return None

        report_rows = []

        # Determine mode: single, bulk-by-list, or bulk-by-file
        if file_path:
            # bulk via CSV file; group may be provided as global or per-row
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group

            User = get_user_model()

            group_global = group_name
            assigned = 0
            with open(file_path, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                # Accept files with header 'username' or 'email' and optional 'group'
                for row in reader:
                    ident = (row.get("username") or row.get("email") or "").strip()
                    if not ident:
                        continue
                    gname = (row.get("group") or group_global or "").strip()
                    if not gname:
                        report_rows.append(
                            {
                                "ident": ident,
                                "group": "",
                                "status": "skipped",
                                "reason": "no_group",
                            }
                        )
                        self.stdout.write(f"Skipping {ident}: no group provided\n")
                        continue
                    user = _find_user(User, ident)
                    if not user:
                        report_rows.append(
                            {"ident": ident, "group": gname, "status": "not_found"}
                        )
                        self.stdout.write(f"User '{ident}' not found; skipping\n")
                        continue
                    group, _ = Group.objects.get_or_create(name=gname)
                    if dry_run:
                        report_rows.append(
                            {
                                "ident": ident,
                                "user": str(user),
                                "group": gname,
                                "status": "would_assign",
                            }
                        )
                        self.stdout.write(
                            f"[dry-run] Would add {user} to group '{gname}'\n"
                        )
                    else:
                        group.user_set.add(user)
                        assigned += 1
                        report_rows.append(
                            {
                                "ident": ident,
                                "user": str(user),
                                "group": gname,
                                "status": "assigned",
                            }
                        )

            # if no report_file requested but we have report_rows, auto-generate filename
            if not report_file and report_rows:
                report_file = generate_report_path(
                    prefix="reports/proje_assign", ext=report_format
                )

            # if no explicit report_file provided but we have report_rows, auto-generate into MEDIA_ROOT
            if not report_file and report_rows:
                report_file = generate_report_path(
                    prefix="reports/proje_assign",
                    ext=report_format,
                    label=label or group_global,
                )

            if report_file:
                media_root = getattr(
                    __import__("django.conf").conf.settings, "MEDIA_ROOT", None
                )
                target_path = Path(report_file)
                if not target_path.is_absolute() and media_root:
                    target_path = Path(media_root) / report_file
                target_path.parent.mkdir(parents=True, exist_ok=True)
                if report_format == "csv":
                    keys = ["ident", "user", "group", "status", "reason"]
                    with target_path.open("w", newline="", encoding="utf-8") as outfh:
                        writer = csv.DictWriter(outfh, fieldnames=keys)
                        writer.writeheader()
                        for r in report_rows:
                            writer.writerow({k: r.get(k, "") for k in keys})
                else:
                    with target_path.open("w", encoding="utf-8") as outfh:
                        json.dump(report_rows, outfh, ensure_ascii=False, indent=2)

                # Optionally upload to S3
                if upload_s3:
                    try:
                        from proje.utils import upload_file_to_s3

                        bucket = s3_bucket
                        # If bucket not provided via arg, try settings
                        if not bucket:
                            bucket = getattr(
                                __import__("django.conf").conf.settings,
                                "REPORTS_S3_BUCKET",
                                None,
                            )
                        res = upload_file_to_s3(
                            target_path, bucket=bucket, key=s3_key, public=s3_public
                        )
                        self.stdout.write(f"Uploaded report to S3: {res.get('url')}\n")
                    except Exception as exc:  # pragma: no cover - best-effort upload
                        self.stderr.write(f"Failed to upload report to S3: {exc}\n")

            if dry_run:
                self.stdout.write(f"[dry-run] Processed CSV {file_path}\n")
            else:
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
                user = _find_user(User, ident)
                if not user:
                    report_rows.append(
                        {"ident": ident, "group": group_name, "status": "not_found"}
                    )
                    self.stdout.write(f"User '{ident}' not found; skipping\n")
                    continue
                group, _ = Group.objects.get_or_create(name=group_name)
                if dry_run:
                    report_rows.append(
                        {
                            "ident": ident,
                            "user": str(user),
                            "group": group_name,
                            "status": "would_assign",
                        }
                    )
                    self.stdout.write(
                        f"[dry-run] Would add {user} to group '{group_name}'\n"
                    )
                else:
                    group.user_set.add(user)
                    assigned += 1
                    report_rows.append(
                        {
                            "ident": ident,
                            "user": str(user),
                            "group": group_name,
                            "status": "assigned",
                        }
                    )

            # if no report_file requested but we have report_rows, auto-generate filename
            if not report_file and report_rows:
                report_file = generate_report_path(
                    prefix="reports/proje_assign", ext=report_format
                )

            # write report if requested
            # if no explicit report_file provided but we have report_rows, auto-generate into MEDIA_ROOT
            if not report_file and report_rows:
                report_file = generate_report_path(
                    prefix="reports/proje_assign", ext=report_format, label=label
                )

            if report_file:
                media_root = getattr(
                    __import__("django.conf").conf.settings, "MEDIA_ROOT", None
                )
                target_path = Path(report_file)
                if not target_path.is_absolute() and media_root:
                    target_path = Path(media_root) / report_file
                target_path.parent.mkdir(parents=True, exist_ok=True)
                if report_format == "csv":
                    keys = ["ident", "user", "group", "status"]
                    with target_path.open("w", newline="", encoding="utf-8") as outfh:
                        writer = csv.DictWriter(outfh, fieldnames=keys)
                        writer.writeheader()
                        for r in report_rows:
                            writer.writerow({k: r.get(k, "") for k in keys})
                else:
                    with target_path.open("w", encoding="utf-8") as outfh:
                        json.dump(report_rows, outfh, ensure_ascii=False, indent=2)

                # Optionally upload to S3
                if upload_s3:
                    try:
                        from proje.utils import upload_file_to_s3

                        bucket = s3_bucket
                        if not bucket:
                            bucket = getattr(
                                __import__("django.conf").conf.settings,
                                "REPORTS_S3_BUCKET",
                                None,
                            )
                        res = upload_file_to_s3(
                            target_path, bucket=bucket, key=s3_key, public=s3_public
                        )
                        self.stdout.write(f"Uploaded report to S3: {res.get('url')}\n")
                    except Exception as exc:  # pragma: no cover - best-effort upload
                        self.stderr.write(f"Failed to upload report to S3: {exc}\n")

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

        # resolve by username or email
        user = _find_user(User, username)
        if not user:
            raise CommandError(f"User '{username}' not found")

        group, _ = Group.objects.get_or_create(name=group_name)
        if dry_run:
            report_rows.append(
                {
                    "ident": username,
                    "user": str(user),
                    "group": group_name,
                    "status": "would_assign",
                }
            )
            self.stdout.write(f"[dry-run] Would add {user} to group '{group_name}'\n")
        else:
            group.user_set.add(user)
            report_rows.append(
                {
                    "ident": username,
                    "user": str(user),
                    "group": group_name,
                    "status": "assigned",
                }
            )
            # Use plain write to avoid type issues in static analysis
            self.stdout.write(f"Added user {user} to group '{group_name}'\n")

        # if no report_file requested but we have report_rows, auto-generate filename
        if not report_file and report_rows:
            report_file = generate_report_path(
                prefix="reports/proje_assign", ext=report_format
            )

        # if no explicit report_file provided but we have report_rows, auto-generate into MEDIA_ROOT
        if not report_file and report_rows:
            report_file = generate_report_path(
                prefix="reports/proje_assign", ext=report_format, label=label
            )

        if report_file:
            media_root = getattr(
                __import__("django.conf").conf.settings, "MEDIA_ROOT", None
            )
            target_path = Path(report_file)
            if not target_path.is_absolute() and media_root:
                target_path = Path(media_root) / report_file
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if report_format == "csv":
                keys = ["ident", "user", "group", "status"]
                with target_path.open("w", newline="", encoding="utf-8") as outfh:
                    writer = csv.DictWriter(outfh, fieldnames=keys)
                    writer.writeheader()
                    for r in report_rows:
                        writer.writerow({k: r.get(k, "") for k in keys})
            else:
                with target_path.open("w", encoding="utf-8") as outfh:
                    json.dump(report_rows, outfh, ensure_ascii=False, indent=2)

            # Optionally upload to S3
            if upload_s3:
                try:
                    from proje.utils import upload_file_to_s3

                    bucket = s3_bucket
                    if not bucket:
                        bucket = getattr(
                            __import__("django.conf").conf.settings,
                            "REPORTS_S3_BUCKET",
                            None,
                        )
                    res = upload_file_to_s3(
                        target_path, bucket=bucket, key=s3_key, public=s3_public
                    )
                    self.stdout.write(f"Uploaded report to S3: {res.get('url')}\n")
                except Exception as exc:  # pragma: no cover - best-effort upload
                    self.stderr.write(f"Failed to upload report to S3: {exc}\n")
