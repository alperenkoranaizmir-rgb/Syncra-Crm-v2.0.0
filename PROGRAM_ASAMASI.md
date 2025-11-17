# Program Aşaması

Bu doküman projeyi geliştirme sürecinde izlenen adımları ve ilerleme aşamalarını adım adım özetler.

1. Proje Başlangıcı
   - Django projesi (`config/`) ve temel `core` uygulaması oluşturuldu.
   - Türkçe lokalizasyon ayarlandı (`LANGUAGE_CODE='tr'`, `TIME_ZONE='Europe/Istanbul'`).

2. AdminLTE Entegrasyonu
   - AdminLTE teması ve plugin'leri yerel statik dosya olarak projeye entegre edildi.
   - AdminLTE demo sayfalarının bir kısmı `templates/pages/` altına kopyalandı.

3. Demo Sayfalarını Ekleme ve Plugin Konfigürasyonu
   - DataTables, Chart.js, FullCalendar, Ekko Lightbox, Summernote vb. pluginler template'lerde init edildi.
   - Tüm plugin bağımlılıklarının local static yolları (`{% static 'admin-lte/plugins/...' %}`) kullanıldı.

4. Otomasyon ve Kalite Araçları
   - `.github/workflows/ci.yml` ile CI eklendi: bağımlılık yükleme, `collectstatic` ve `python manage.py test` adımları.
   - `.pre-commit-config.yaml` ile pre-commit hooks eklendi (black, isort, flake8, mypy, bandit) ve bandit taraması proje dizinleriyle sınırlandırıldı.

5. Statik Dosya Çatışmaları ve Araçlar
   - `collectstatic` sırasında duplicate-destination uyarıları görüldü; tespit için yardımcı scriptler (ör. `scripts/list_static_conflicts.py`) eklendi.
   - Gerekli çakışma tespiti ve minimal overrides ile statik varlıkların kullanılabilirliği sağlandı.

6. Pixel-Perfect Düzeltmeler
   - Öncelik sırasına göre demo sayfalarında görsel düzeltmeler yapıldı: `DataTables`, `ChartJS`, `FullCalendar`, `Gallery`, `Mailbox`, `Dashboard` gibi sayfalar güncellendi.
   - Her sayfa için küçük CSS override dosyaları `static/css/*.css` altında eklendi.

7. Test ve Doğrulama
   - Birim ve entegrasyon testleri (`python manage.py test`) eklendi ve çalıştırıldı.
   - Tüm yapılan değişiklikler testler ile kontrol edilip commitlendi.

8. Sonraki Adımlar (özet)
   - Dashboard ve diğer demo sayfaların pixel-perfect final geçişi.
   - Statik çakışma politikası belirlenmesi (hangi kaynağın tercih edileceği).
   - Uzak repoya push & PR süreci tamamlanması.

---
Bu dosya proje ilerledikçe güncellenecektir.


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
