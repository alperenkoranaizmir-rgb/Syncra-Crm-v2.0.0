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
