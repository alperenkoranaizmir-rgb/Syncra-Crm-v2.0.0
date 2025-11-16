import csv
import io
import json
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings

User = get_user_model()


class TestProjeAssignGroupCommand(TestCase):
    def _read_report(self, path: Path):
        if path.suffix == ".json":
            return json.loads(path.read_text(encoding="utf-8"))
        rows = []
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for r in reader:
                rows.append(r)
        return rows

    def test_single_user_assign_creates_group_and_report(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir):
            User.objects.create_user("alice", email="alice@example.com", password="pw")
            out = io.StringIO()
            call_command(
                "proje_assign_group",
                "--username",
                "alice",
                "--group",
                "Proje Yöneticisi",
                stdout=out,
            )
            self.assertIn("Added user", out.getvalue())

            # report should be generated under MEDIA_ROOT/reports
            reports_dir = Path(settings.MEDIA_ROOT) / "reports"
            self.assertTrue(reports_dir.exists())
            files = list(reports_dir.glob("proje_assign*.*"))
            self.assertTrue(files, "Expected at least one auto-generated report file")
            report = files[0]
            data = self._read_report(report)
            # single user report contains one row with assigned status
            self.assertTrue(any(r.get("status") == "assigned" for r in data))

    def test_users_list_dry_run_and_json_report(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir):
            User.objects.create_user("bob", email="bob@example.com", password="pw")
            User.objects.create_user("carol", email="carol@example.com", password="pw")
            out = io.StringIO()
            call_command(
                "proje_assign_group",
                "--users",
                "bob,carol,missing@example.com",
                "--group",
                "TestGroup",
                "--dry-run",
                "--report-format",
                "json",
                stdout=out,
            )
            self.assertIn("Would add", out.getvalue())

            reports_dir = Path(settings.MEDIA_ROOT) / "reports"
            self.assertTrue(reports_dir.exists())
            files = list(reports_dir.glob("proje_assign*.*"))
            self.assertTrue(files)
            report = files[0]
            self.assertEqual(report.suffix, ".json")
            data = self._read_report(report)
            # should contain would_assign entries and not actually add users
            self.assertTrue(any(r.get("status") == "would_assign" for r in data))
            # ensure users are not members of the group in dry-run
            from django.contrib.auth.models import Group

            g = Group.objects.filter(name="TestGroup").first()
            if g:
                self.assertFalse(g.user_set.filter(username="bob").exists())

    def test_file_csv_assign_per_row_group_and_not_found(self):
        tmpdir = tempfile.mkdtemp()
        csv_path = Path(tmpdir) / "input.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["username", "group"])
            writer.writerow(["dave", "GroupA"])
            writer.writerow(["eve@example.com", "GroupB"])

        with override_settings(MEDIA_ROOT=tmpdir):
            User.objects.create_user("dave", email="dave@example.com", password="pw")
            # note: eve (by email) does not exist; should be reported as not_found
            out = io.StringIO()
            call_command("proje_assign_group", "--file", str(csv_path), stdout=out)
            self.assertIn("Assigned", out.getvalue() or "")

            reports_dir = Path(settings.MEDIA_ROOT) / "reports"
            self.assertTrue(reports_dir.exists())
            files = list(reports_dir.glob("proje_assign*.*"))
            self.assertTrue(files)
            report = files[0]
            data = self._read_report(report)
            # should have an assigned row for dave and a not_found for eve
            statuses = [r.get("status") for r in data]
            self.assertIn("assigned", statuses)
            self.assertIn("not_found", statuses)

    def test_upload_to_s3_called_when_requested(self):
        # Patch the upload_file_to_s3 helper to avoid real AWS calls
        from unittest.mock import patch

        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir):
            User.objects.create_user("frank", email="frank@example.com", password="pw")
            out = io.StringIO()
            with patch("proje.utils.upload_file_to_s3") as mock_upload:
                mock_upload.return_value = {
                    "url": "https://example.com/report.csv",
                    "bucket": "b",
                    "key": "k",
                }
                call_command(
                    "proje_assign_group",
                    "--username",
                    "frank",
                    "--group",
                    "S3Group",
                    "--upload-s3",
                    "--s3-bucket",
                    "test-bucket",
                    stdout=out,
                )
                # upload helper should have been called once
                self.assertTrue(mock_upload.called)
                self.assertIn("Uploaded report to S3", out.getvalue())
