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


## 2025-11-17 04:33:47 UTC — Hooks enabled: automatic changelog updates


## 2025-11-17 04:35:06 UTC — Make script timezone-aware


## 2025-11-17 04:35:29 UTC — ci: run changelog updater in CI; make script timezone-aware


## 2025-11-17 04:36:59 UTC — chore: run changelog updater only on success; add onboarding script to enable hooks


## 2025-11-17 04:48:04 UTC — chore(scripts): add docstrings to update_changelogs functions


## 2025-11-17 04:51:21 UTC — chore(lint): narrow broad except clauses and add targeted pylint disables


## 2025-11-17 04:58:11 UTC — chore(lint): narrow script excepts, add docstrings for scripts, add pylint to CI


## 2025-11-17 05:04:57 UTC — chore(docs): add module docstrings and admin QA helper


## 2025-11-17 05:05:45 UTC — ci: set DJANGO_SETTINGS_MODULE at job level for tests & lint


## 2025-11-17 05:08:02 UTC — scripts: make admin_qa robust to DisallowedHost by setting HTTP_HOST


## 2025-11-17 05:12:58 UTC — refactor(admin): extract report write/upload helpers and simplify owner assign action


## 2025-11-17 05:13:34 UTC — chore(docs/refactor): add admin class docstrings and remove unused imports


## 2025-11-17 05:14:12 UTC — chore(docs): add helper docstrings and utils module docstring; wrap long signature

