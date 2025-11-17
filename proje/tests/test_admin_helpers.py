from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
import tempfile

from proje.models import Document
from proje import admin_helpers
from django.contrib.auth.models import Group
from types import SimpleNamespace
from django.utils.datastructures import MultiValueDict
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages.storage.cookie import CookieStorage
from proje.models import Project, Owner

User = get_user_model()


class AdminHelpersTests(TestCase):
    def test_format_file_link_html_renders_link_and_metadata(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir, MEDIA_URL="/media/"):
            user = User.objects.create_user("tester2", email="t2@test.local", password="pw")
            img = SimpleUploadedFile("photo2.jpg", b"\x89PNG\r\n\x1a\n", content_type="image/png")
            doc = Document.objects.create(file=img, label="Foto2", uploaded_by=user)

            html = str(admin_helpers.format_file_link_html(doc))
            self.assertIn("<a ", html)
            self.assertIn("data-size=", html)
            self.assertIn("data-uploader=", html)

    def test_format_preview_html_image_and_non_image(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir, MEDIA_URL="/media/"):
            user = User.objects.create_user("tester3", email="t3@test.local", password="pw")
            img = SimpleUploadedFile("photo3.png", b"\x89PNG\r\n\x1a\n", content_type="image/png")
            doc_img = Document.objects.create(file=img, label="Img3", uploaded_by=user)

            html = str(admin_helpers.format_preview_html(doc_img))
            self.assertIn("<img", html)

            pdf = SimpleUploadedFile("doc3.pdf", b"%PDF-1.4\n%", content_type="application/pdf")
            doc_pdf = Document.objects.create(file=pdf, label="Doc3", uploaded_by=user)
            html2 = str(admin_helpers.format_preview_html(doc_pdf))
            self.assertNotIn("<img", html2)
            self.assertIn('target="_blank"', html2)

    def test_create_documents_from_files_creates_instances(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir, MEDIA_URL="/media/"):
            user = User.objects.create_user("tester4", email="t4@test.local", password="pw")
            f1 = SimpleUploadedFile("a.txt", b"hello")
            f2 = SimpleUploadedFile("b.txt", b"world")
            created = admin_helpers.create_documents_from_files([f1, f2], ["A", "B"], None, None, user)
            self.assertEqual(len(created), 2)
            self.assertTrue(all(isinstance(d, Document) for d in created))

    def test_process_bulk_document_upload_creates_documents_and_redirects(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir, MEDIA_URL="/media/"):
            user = User.objects.create_user("uploader", email="uploader@test.local", password="pw")
            f1 = SimpleUploadedFile("a.txt", b"hello")
            f2 = SimpleUploadedFile("b.txt", b"world")
            post = {"labels": "A\nB", "uploaded_by": str(user.pk)}
            files = MultiValueDict({"files": [f1, f2]})
            # Use a lightweight fake request and admin_instance for the helper
            req = SimpleNamespace(method="POST", POST=post, FILES=files, user=user)
            admin_instance = SimpleNamespace(message_user=lambda *a, **k: None, model=Document)
            from proje.admin_forms import DocumentBulkUploadForm
            # sanity-check the form validity to catch why process may not create docs
            form = DocumentBulkUploadForm(req.POST, req.FILES)
            self.assertTrue(form.is_valid(), msg=str(form.errors))
            # ensure files made it into our fake request.FILES as expected
            self.assertIn("files", req.FILES)
            self.assertEqual(len(req.FILES.getlist("files")), 2)
            redirect_url, created = admin_helpers.process_bulk_document_upload(req, DocumentBulkUploadForm, admin_instance)
            self.assertIsNotNone(redirect_url)
            self.assertEqual(created, 2)

    def test_perform_owner_assignment_dry_run_and_assign(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir, MEDIA_URL="/media/"):
            # prepare users and owners
            user_a = User.objects.create_user("u_a", email="a@test.local", password="pw")
            proj = Project.objects.create(name="TP", code="TP1")
            owner_with_email = Owner.objects.create(first_name="A", last_name="B", email="a@test.local", project=proj)
            owner_no_email = Owner.objects.create(first_name="X", last_name="Y", email="", project=proj)
            grp = Group.objects.create(name="TTest")
            # dry-run
            post = {"group": str(grp.pk), "dry_run": "on", "report_format": "csv"}
            rf = RequestFactory()
            req = rf.post("/", data=post)
            req.user = user_a
            req._messages = CookieStorage(req)
            admin_instance = __import__("django.contrib.admin").contrib.admin.site._registry.get(Owner)  # noqa: W901
            tpl_ctx = admin_helpers.perform_owner_assignment(req, __import__("proje.models", fromlist=["Owner"]).Owner.objects.all(), admin_instance)
            self.assertIsNotNone(tpl_ctx)
            tpl, ctx = tpl_ctx
            self.assertIn("report_rows", ctx)
            # actual assign
            post2 = {"group": str(grp.pk), "report_format": "csv"}
            req2 = rf.post("/", data=post2)
            req2.user = user_a
            req2._messages = CookieStorage(req2)
            tpl_ctx2 = admin_helpers.perform_owner_assignment(req2, Owner.objects.all(), admin_instance)
            self.assertIsNotNone(tpl_ctx2)
            # group should have user a assigned if email matched
            self.assertIn(user_a, grp.user_set.all())
