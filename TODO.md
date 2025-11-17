# TODO (Canlı Liste)

Bu dosya otomatik olarak `scripts/todo_state.json` dosyasından üretilir.

## Tamamlanan (✔)

- ✔ AdminLTE demo şablonları ekleme — templates/pages/ altında demo sayfaları eklendi.
- ✔ DataTables pixel-perfect — DataTables Buttons, TR dil ayarları ve CSS overrides eklendi.
- ✔ ChartJS demo düzenleme — Area/Doughnut chart init ve CSS overrides eklendi.
- ✔ FullCalendar entegrasyonu — TR locale, toolbar ve CSS overrides eklendi.
- ✔ Gallery (Ekko Lightbox) — Galeri grid ve lightbox init eklendi.
- ✔ Mailbox UI — Inbox layout, compose modal ve JS eklendi.
- ✔ Uzak repoya final push/PR — Son kontrol ve PR hazırlama.

## Devam Eden / Yapılmakta

- ⏳ Dashboard pixel-perfect — Dashboard'un final pixel-perfect düzeltmeleri (devam ediyor)

## Beklemede / Başlanmamış

- ☐ Statik çakışma politikası — collectstatic duplicate-destination politikası belirleme ve uygulama.

---
Bu dosya otomatik olarak güncellenebilir: `python scripts/update_todo_md.py set <id> <completed|in-progress|not-started>`


### Son Değişiklikler (2025-11-17):
- Seed changelog: pixel-perfect & admin updates

### Son Değişiklikler (2025-11-17):
- Hooks enabled: automatic changelog updates

### Son Değişiklikler (2025-11-17):
- Make script timezone-aware

### Son Değişiklikler (2025-11-17):
- ci: run changelog updater in CI; make script timezone-aware

### Son Değişiklikler (2025-11-17):
- chore: run changelog updater only on success; add onboarding script to enable hooks

### Son Değişiklikler (2025-11-17):
- chore(scripts): add docstrings to update_changelogs functions

### Son Değişiklikler (2025-11-17):
- chore(lint): narrow broad except clauses and add targeted pylint disables

### Son Değişiklikler (2025-11-17):
- chore(lint): narrow script excepts, add docstrings for scripts, add pylint to CI

### Son Değişiklikler (2025-11-17):
- chore(docs): add module docstrings and admin QA helper

### Son Değişiklikler (2025-11-17):
- ci: set DJANGO_SETTINGS_MODULE at job level for tests & lint

### Son Değişiklikler (2025-11-17):
- scripts: make admin_qa robust to DisallowedHost by setting HTTP_HOST

### Son Değişiklikler (2025-11-17):
- refactor(admin): extract report write/upload helpers and simplify owner assign action

### Son Değişiklikler (2025-11-17):
- chore(docs/refactor): add admin class docstrings and remove unused imports

### Son Değişiklikler (2025-11-17):
- chore(docs): add helper docstrings and utils module docstring; wrap long signature

### Son Değişiklikler (2025-11-17):
- chore(admin): split add_view, move imports, reduce pylint warnings

### Son Değişiklikler (2025-11-17):
- chore(migrations): docstrings and safer reverse delete handling for groups migration

### Son Değişiklikler (2025-11-17):
- chore(admin): extract owner-assignment helper, move imports to module level, reduce lint warnings

### Son Değişiklikler (2025-11-17):
- refactor(admin): import perform_owner_assignment, remove unused helper imports

### Son Değişiklikler (2025-11-17):
- refactor(admin): extract process_bulk_document_upload helper and use in DocumentAdmin.add_view; reorder imports

### Son Değişiklikler (2025-11-17):
- chore(admin): narrow broad-except for S3/upload errors; chore(migrations): add short module docstrings

### Son Değişiklikler (2025-11-17):
- chore(lint): reorder imports and add migration class docstrings

### Son Değişiklikler (2025-11-17):
- chore(admin): add admin UI snapshot

### Son Değişiklikler (2025-11-17):
- refactor(admin): extract admin forms to proje.admin_forms

### Son Değişiklikler (2025-11-17):
- style(admin): move admin forms to module and remove unused imports
