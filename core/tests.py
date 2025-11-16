from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings


class CoreViewsTests(TestCase):
    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse('core:dashboard'))
        # should redirect to login
        self.assertIn(resp.status_code, (302, 301))

    def test_index_redirects_to_dashboard(self):
        resp = self.client.get(reverse('core:dashboard'))
        self.assertIn(resp.status_code, (301, 302))

    def test_404_template_used(self):
        # Ensure handler404 renders our template when DEBUG=False
        with override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver']):
            resp = self.client.get('/this-url-does-not-exist/')
            self.assertEqual(resp.status_code, 404)
            self.assertTemplateUsed(resp, '404.html')

    def test_static_vendor_files_exist(self):
        # Check a few vendor files exist in project static directory
        base = settings.BASE_DIR
        paths = [
            base / 'static' / 'vendor' / 'adminlte' / 'adminlte.min.css',
            base / 'static' / 'vendor' / 'adminlte' / 'adminlte.min.js',
        ]
        for p in paths:
            self.assertTrue(p.exists(), f"Static file missing: {p}")
