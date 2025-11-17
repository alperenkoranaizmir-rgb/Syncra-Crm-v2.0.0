"""Tests for the Document admin preview helper.

Verifies that image documents render an inline preview and that
non-image documents render a link target.
"""
# pylint: disable=missing-function-docstring

import tempfile

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from proje.models import Document

User = get_user_model()


class DocumentAdminPreviewTests(TestCase):
    """Ensure admin preview renders image previews and links for others."""
    def test_preview_includes_metadata_for_images_and_links_for_non_images(self):
        tmpdir = tempfile.mkdtemp()
        with override_settings(MEDIA_ROOT=tmpdir, MEDIA_URL="/media/"):
            user = User.objects.create_user(
                "tester", email="t@test.local", password="pw"
            )

            admin_instance = admin.site._registry.get(Document)  # pylint: disable=protected-access
            self.assertIsNotNone(
                admin_instance, "Document admin must be registered for the test"
            )

            # create an image file
            img = SimpleUploadedFile(
                "photo.jpg", b"\x89PNG\r\n\x1a\n", content_type="image/png"
            )
            doc_img = Document.objects.create(file=img, label="Foto", uploaded_by=user)

            html = str(admin_instance.preview(doc_img))
            # should render an <img> within an anchor and include metadata attributes
            self.assertIn("<img", html)
            self.assertIn("data-size=", html)
            self.assertIn("data-uploader=", html)

            # create a non-image file
            pdf = SimpleUploadedFile(
                "doc.pdf", b"%PDF-1.4\n%", content_type="application/pdf"
            )
            doc_pdf = Document.objects.create(
                file=pdf, label="Sözleşme", uploaded_by=user
            )
            html2 = str(admin_instance.preview(doc_pdf))
            # should not render an <img>, but a clickable link
            self.assertNotIn("<img", html2)
            self.assertIn('target="_blank"', html2)
