# CHANGELOG

Bu dosya proje içi önemli değişiklikleri kronolojik olarak kaydeder. `scripts/update_changelogs.py` script'i ile otomatik güncellenebilir.

## 2025-11-17 — Pixel-perfect & Admin improvements
- Add `static/css/pixel_perfect.css` and include in `templates/base.html` to provide global visual overrides.
- Updated dashboard and demo pages: added `gap-fix` utility class to normalize spacing.
- Added `proje/admin_helpers.py` (`AdminBootstrapMixin`) to standardize admin form controls.
- Added `proje/management/commands/load_demo_data.py` to seed demo users, projects, owners, units, and a sample document.
- Fixed `MEDIA_URL` / `MEDIA_ROOT` defaults in `config/settings.py` to avoid admin URL conflicts.
- Tests run locally (pytest) and changes were committed and pushed to `main`.

---


## 2025-11-17 04:30:19 UTC — Seed changelog: pixel-perfect & admin updates

