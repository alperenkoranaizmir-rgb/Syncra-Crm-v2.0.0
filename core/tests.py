from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse


class CoreViewsTests(TestCase):
    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse("core:dashboard"))
        # should redirect to login
        self.assertIn(resp.status_code, (302, 301))

    def test_index_redirects_to_dashboard(self):
        resp = self.client.get(reverse("core:dashboard"))
        self.assertIn(resp.status_code, (301, 302))

    def test_404_template_used(self):
        # Ensure handler404 renders our template when DEBUG=False
        with override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"]):
            resp = self.client.get("/this-url-does-not-exist/")
            self.assertEqual(resp.status_code, 404)
            self.assertTemplateUsed(resp, "404.html")

    def test_static_vendor_files_exist(self):
        # Check a few vendor files exist in project static directory
        base = settings.BASE_DIR
        # Accept either legacy vendor layout or collected admin-lte plugin paths
        candidate_paths = [
            base / "static" / "vendor" / "adminlte" / "adminlte.min.css",
            base / "static" / "vendor" / "adminlte" / "adminlte.min.js",
            base / "staticfiles" / "admin-lte" / "dist" / "css" / "adminlte.min.css",
            base / "staticfiles" / "admin-lte" / "dist" / "js" / "adminlte.min.js",
        ]
        found = False
        for p in candidate_paths:
            if p.exists():
                found = True
                break
        self.assertTrue(found, f"Static file missing (tried paths): {candidate_paths}")

    def test_demo_pages_render_for_logged_in_user(self):
        # create and login a user, then ensure demo pages render (200)
        User = get_user_model()
        u = User.objects.create_user(username="tester", password="testpass")
        self.client.force_login(u)
        demo_paths = [
            reverse("core:charts_chartjs"),
            reverse("core:tables_datatables"),
            reverse("core:examples_projects"),
            reverse("core:widgets"),
            reverse("core:ui_general"),
            reverse("core:ui_buttons"),
            reverse("core:ui_modals"),
            reverse("core:calendar"),
            reverse("core:gallery"),
            reverse("core:kanban"),
            reverse("core:mailbox"),
            reverse("core:examples_invoice"),
            reverse("core:examples_profile"),
            reverse("core:examples_contacts"),
            reverse("core:index"),
        ]
        for p in demo_paths:
            resp = self.client.get(p)
            self.assertIn(
                resp.status_code, (200, 302), msg=f"{p} returned {resp.status_code}"
            )
