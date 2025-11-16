# Hatalar ve Durumları

Aşağıda geliştirme sürecinde görülen hatalar, tetkikler ve çözüm durumları listelenmiştir.

1. Template `{% static %}` tag eksikliği
   - Dosya: `templates/pages/charts/chartjs.html` gibi bazı şablonlarda `{% load static %}` eksikti.
   - Durum: Çözüldü — `{% load static %}` eklendi.

2. `collectstatic` duplicate-destination uyarıları
   - Sebep: AdminLTE paketinden gelen bazı statik dosyalar ile Django admin veya diğer paketlerin aynı hedef path'e sahip olması.
   - Durum: Tespit için scriptler eklendi (`scripts/list_static_conflicts.py`). Politikayı kesinleştirmek gerekiyor (ör. AdminLTE önceliği veya özel override dizini).

3. Bandit taraması site-packages taraması nedeniyle hata veriyordu
   - Sebep: Güvenlik tarayıcısı bazı üçüncü taraf paketlerin AST'sini işlerken hata üretiyordu.
   - Durum: Bandit taramaları proje dizinleriyle sınırlanarak sorun atlatıldı; proje düzeyindeki güvenlik uyarıları ayrı incelendi.

4. Geniş `except: pass` ve hardcoded test parolası uyarıları
   - Dosya: `core/tests.py` ve benzeri
   - Durum: `except` blokları daraltıldı; test parolaları `secrets` ile üretildi — uyarılar kapatıldı.

5. Template bloklarının (duplicate block) hatalı kullanımı
   - Örnek: `templates/pages/calendar.html`'de `extra_css` bloğu iki kez tanımlanmıştı.
   - Durum: Duplicate bloklar birleştirildi.

6. Diğer küçük hatalar
   - Birkaç linter uyarısı (flake8/mypy) düzeltildi; import/format ve değişken isimlendirme sorunları giderildi.

---
Hataların çoğu düzeltildi; kalan eylem: statik çakışma politikasını netleştirip repo seviyesinde uygulanması.
