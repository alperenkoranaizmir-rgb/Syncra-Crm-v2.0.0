# Template Dokümantasyonu

Bu dosya `templates/` dizinindeki önemli şablonların kısa açıklamalarını ve nerede kullanıldıklarını içerir.

- `templates/base.html`
  - Projenin ana base şablonu; `adminlte/base.html`'i genişletir.
  - Ortak CSS/JS include'larını ve `syncraAlert` helper'larını içerir.

- `templates/pages/dashboard.html`
  - Dashboard ana sayfası; küçük kutucuklar (`small-box`) ve kartlar içerir.
  - AdminLTE demo görünümüne göre düzenlendi.

- `templates/pages/charts/chartjs.html`
  - Chart.js demo sayfası (Area & Donut örnekleri).
  - `{% load static %}` içermelidir; `extra_css`/`extra_js` blokları ile override edilir.

- `templates/pages/tables/data.html`
  - DataTables demo; butonlar ve export (Buttons) plugin'leri için init kodu içerir.

- `templates/pages/calendar.html`
  - FullCalendar demo; `locales-all.min.js` ile Türkçe yerelleştirme ve toolbar yapılandırması yapılmıştır.

- `templates/pages/gallery.html`
  - Ekko Lightbox tabanlı galeri; küçük resimler grid olarak yer alır, lightbox için `data-gallery` kullanılır.

- `templates/pages/mailbox/mailbox.html`
  - Mailbox demo: sol panel (folders), gelen kutusu tablosu ve compose modal.

Genel Kullanım Notları
- Her child template `base.html`'i genişletir ve gerekirse `{% load static %}` eklemelidir.
- Stil düzeltmeleri `static/css/` altındaki özel dosyalarda toplanmıştır; bu dosyalar `extra_css` içinde include edilir.
- Plugin JS dosyaları `base.html` içinde veya ilgili şablonun `extra_js` bloğunda yüklenecek; mümkün olduğunda global inclusion `base.html`'de yapıldı.


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

### Son Değişiklikler (2025-11-17):
- accounts: add app, fix lint warnings, update .pylintrc; run tests locally

### Son Değişiklikler (2025-11-17):
- ci: quote python-version matrix entries to avoid numeric parsing issues

### Son Değişiklikler (2025-11-17):
- CI: fix requirements - relax boto3 pin to allow install on runners

### Son Değişiklikler (2025-11-17):
- accounts: ensure __str__ returns str (pylint fix)

### Son Değişiklikler (2025-11-17):
- proje: add docstrings, fix pylint naming and disable django-not-configured

### Son Değişiklikler (2025-11-17):
- accounts: cleanup create_accounts_defaults imports, docstring, fix unused vars and output formatting

### Son Değişiklikler (2025-11-17):
- tests: tidy imports, add module docstring and suppress test-only pylint warnings

### Son Değişiklikler (2025-11-17):
- tests: add module and class docstrings for document admin preview tests

### Son Değişiklikler (2025-11-17):
- scripts: rename User variable to user_model (pylint fix)
