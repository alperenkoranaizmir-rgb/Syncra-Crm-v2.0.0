# Syncra CRM v2.0.0

Kısa açıklama
- Syncra CRM: Kurumsal müşteri ilişkileri yönetimi (CRM) uygulamasının Django tabanlı sürümü.

Önemli not
- Bu proje yerel geliştirme ve dağıtım amaçlıdır. Aşağıdaki komutlar ve adımlar tipik bir Django projesi için genel rehberdir; projeye özgü ek yapılandırmalar `settings`, `.env` veya `deployment` dokümanlarında bulunabilir.

Gereksinimler
- Python 3.8+ (sanal ortam önerilir)
- `pip`
- (Opsiyonel) `virtualenv` veya `venv`
 - Proje bağımlılıkları `requirements.txt` dosyasında listelenir. Yeni bir paket eklediğinizde önce bu dosyaya ekleyin ve ardından `pip install -r requirements.txt` çalıştırın.

Kurulan paketler
- Aşağıdaki paketler sanal ortamda kuruldu ve `requirements.txt` içine kaydedildi. Tam listeyi proje kökünden `requirements.txt` dosyasında bulabilirsiniz.

- Öne çıkan paketler:
   - `Django==5.2.8` (proje için minimum `Django>=5.0,<6` uyumluluğu sağlandı)
   - `requests` (>=2.28)
   - `celery` (>=5.2)
   - `django-celery-beat` (>=2.4)
   - `WeasyPrint` (>=59.0)
   - `redis` ve `channels`/`channels_redis`
   - `psycopg` / `psycopg2-binary` (Postgres client)
   - `djangorestframework`, `django-filter`, `django-extensions` ve test paketleri (`pytest`, `pytest-django`)

- Notlar:
   - `django-adminlte4-theme` paketi PyPI'de bulunamadı; ancak `django-adminlte4` başarıyla kuruldu. Eğer özel bir tema paketi gerekiyorsa paket adını veya kaynağını kontrol edin.
   - `WeasyPrint` sistem düzeyinde bazı kütüphanelere ihtiyaç duyabilir (ör. `libpango`, `libcairo`, `libgdk-pixbuf`). Eğer PDF oluşturma sırasında hata alırsanız, sistem bağımlılıklarını aşağıdaki gibi yüklemeniz gerekebilir (Debian/Ubuntu örneği):

```bash
sudo apt update
sudo apt install -y build-essential libpango1.0-0 libcairo2 libgdk-pixbuf2.0-0 libffi-dev libxml2 libxslt1.1
```

   - Yeni paket ekledikten sonra sanal ortamda `pip install paket_adı` çalıştırıp `pip freeze > requirements.txt` ile güncelleme yapın.
Hızlı kurulum
1. Depoyu klonlayın veya proje dizinine geçin:

   ```bash
   cd /path/to/Syncra-Crm-v2.0.0
   ```

2. Sanal ortam oluşturun ve etkinleştirin:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   # Sanal ortam etkinleştirildikten sonra Django (ve diğer paketleri) yükleyin:
   pip install "Django>=5.2"
   pip install -r requirements.txt  # (varsa diğer paketleri yükler)
   ```

3. Bağımlılıkları yükleyin (varsa `requirements.txt`):

   ```bash
   pip install -r requirements.txt
   ```

4. Ortam değişkenleri
- Proje kökünde bir `.env` dosyası kullanılıyorsa, gerekli anahtarları (`SECRET_KEY`, `DATABASE_URL` veya DB ayarları, `DEBUG`, vb.) ekleyin. Örnek bir `.env.example` dosyası varsa ona göre kopyalayın ve doldurun.

Veritabanı ve başlangıç
```bash
python manage.py migrate
python manage.py createsuperuser
```

Django dil (Türkçe) ayarları
- Projede Django ayarlarını (`settings.py`) Türkçe yapmak için aşağıdaki ayarları ekleyin/güncelleyin:

```python
# settings.py
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True
# Locale dosyalarını tutmak isterseniz
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_PATHS = [BASE_DIR / 'locale']
```

- Dil dosyalarını oluşturmak için:

```bash
python manage.py makemessages -l tr
python manage.py compilemessages
```

- Not: Sisteminizde Türkçe locale yüklü değilse (`locale-gen tr_TR.UTF-8` gibi) ek olarak işletim sistemi düzeyinde locale eklemeniz gerekebilir.

Bağımlılıklar
- Projenin Python bağımlılıkları `requirements.txt` içinde saklanır. Yeni bir paket eklediğinizde önce sanal ortamda `pip install paket` çalıştırın, ardından güncel paket listesini kaydetmek için:

```bash
pip freeze > requirements.txt
```


Geliştirme sunucusunu çalıştırma
```bash
python manage.py runserver
```

Statik dosyalar (üretim / dağıtım öncesi)
```bash
python manage.py collectstatic
```

Testler
```bash
python manage.py test
```

Yayına hazırlık (özet)
- Ortam değişkenlerini güvenli şekilde ayarlayın.
- `DEBUG=False` ve güvenli `ALLOWED_HOSTS` yapılandırmasını uygulayın.
- Veritabanı, statik ve medya dosyaları için uygun servisleri yapılandırın (Postgres, S3, vs.).

Katkıda bulunma
- Değişiklik yapmadan önce bir issue açın veya mevcut issue'lara yorum yapın.
- Yeni özellikler veya hata düzeltmeleri için ayrı bir branch açın ve açık bir PR oluşturun.

İletişim
- Proje ile ilgili detaylı bilgi veya özel kurulum için proje sahibi ile iletişime geçin.

---
Bu README temel bir başlangıç sağlar. İsterseniz projeye özel kurulum adımlarını, kullanılan paketleri veya deploy rehberini buraya ekleyebilirim.

## AdminLTE Demo Şablonları

Projeye AdminLTE demo sayfalarının birçok örneği eklendi (charts, tables, UI bileşenleri, mailbox, examples, gallery, kanban, calendar, vb.).

- Yeni yollar `core` uygulaması altında tanımlandı; örnek bazı URL'ler:
   - `/core/charts/chartjs/` — ChartJS demo
   - `/core/tables/data/` — DataTables örneği
   - `/core/examples/projects/` — Projects örneği
   - `/core/widgets/`, `/core/ui/buttons/`, `/core/calendar/`, `/core/gallery/` vb.

Bu sayfalar `templates/pages/` altında yer almaktadır ve ileride modüllerde kullanılmak üzere şablon bazlı demo içerik sağlar.

## Hızlı test & deploy adımları

1. Statik dosyaları güncelle:

```bash
python manage.py collectstatic --noinput
```

2. Testleri çalıştır:

```bash
python manage.py test
```

3. Değişiklikleri commitle ve push et:

```bash
git add .
git commit -m "Add AdminLTE demo templates and routes"
git push
```

## Yapılan plugin entegrasyonları

- `DataTables` — tablolarda arama/sıralama/paging desteği (sayfa: `/core/tables/data/`).
- `Chart.js` — grafikler için (sayfa: `/core/charts/chartjs/`).
- `Flot` ve `uPlot` — ek chart örnekleri placeholder ile eklendi.
- `FullCalendar` — takvim entegrasyonu için eklendi ve `calendar` sayfasında başlatıldı.
- `Summernote` — zengin metin editörü `forms/editors` sayfasına entegre edildi.
- `Ekko Lightbox` — `gallery` sayfası için lightbox desteği eklendi.

Not: Bazı demo sayfalar placeholder olarak eklendi; isterseniz aşağıdaki adımlarla hepsini pixel-perfect olarak tamamlayabilirim:
- Detaylı JS init ve stil düzeltmeleri (A).
- Eksik plugin entegrasyonlarının tam ayarlanması (B).
- `requirements.txt` güncellemesi pip-freeze çıktısıyla yapıldı (C).

## CI & pre-commit

Projeye temel bir CI workflow ve yerel pre-commit hook eklendi:

- **GitHub Actions:** `.github/workflows/ci.yml` — push ve pull requestlerde çalışır; Python kurulumu, bağımlılıkların yüklenmesi, `collectstatic --noinput` ve `python manage.py test` adımlarını çalıştırır.
- **Pre-commit:** `.pre-commit-config.yaml` — basit bir yerel hook olarak `python manage.py test` çalıştırır; kullanmak için `pip install pre-commit` ve `pre-commit install` komutlarını çalıştırın.

Kullanım (yerel):

```bash
source .venv/bin/activate
pip install pre-commit
pre-commit install
```

CI çalıştırıldığında testler ve statik toplama otomatik olarak doğrulanır.

## Proje Dokümantasyonu (ek dosyalar)

- `PROGRAM_ASAMASI.md`: Projenin program aşamaları ve adım adım yapılan işler.
- `YAPILAN_ISLER.md`: Bu çalışma sırasında yapılan ana değişikliklerin özeti.
- `HATALAR.md`: Tespit edilen hatalar ve çözümleri (çözülenleri işaretlenmiş).
- `TEMPLATES.md`: `templates/` dizinindeki önemli şablonların açıklamaları ve kullanımları.
- `TODO.md`: Bu zamana kadar oluşturduğum görev listesi ve durumları; ileride tamamlananları buradan güncelleyeceğim.

Dokümanlar repoda root dizininde yer almaktadır. Projeyi klonladıktan sonra bu dosyaları okuyarak yapılan işleri ve kalan görevleri hızlıca görebilirsiniz.
