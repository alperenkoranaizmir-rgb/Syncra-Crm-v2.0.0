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
