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
