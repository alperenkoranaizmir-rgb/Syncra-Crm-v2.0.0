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

Otomatik Changelog Güncelleme
- Lokal geliştirirken her commit'ten sonra bazı markdown dosyalarına (ör. `CHANGELOG.md`, `README.md`, `PROGRAM_ASAMASI.md`, `HATALAR.md`, `TEMPLATES.md`, `TODO.md`, `YAPILAN_ISLER.md`, `YAPILMASI_GEREKENLER.md`, `ONERILER.md`) otomatik bir kısa not eklemek isterseniz repo içindeki git hook şablonunu etkinleştirebilirsiniz.

Etkinleştirme (bir defaya mahsus):
```bash
git config core.hooksPath .githooks
chmod +x .githooks/post-commit
```

Bu işlemden sonra her commit'te `.githooks/post-commit` çalışacak ve `scripts/update_changelogs.py` script'ini çağırarak dosyalara bir "Son Değişiklikler" girdisi ekleyecektir. Manuel çalıştırmak için:

```bash
python3 scripts/update_changelogs.py "Kısa değişiklik açıklaması"
```

Not: Hook'lar yerel `.git/hooks` dizinine uygulanır; eğer CI ortamında otomatik güncelleme isterseniz CI adımlarınıza aynı script'i çağıran bir adım ekleyin.

Kolay onboarding
- Tüm ekip üyelerinin hook'u yerel olarak etkinleştirmesi için repoda bir yardımcı script mevcut: `scripts/onboard.sh`.
- Kullanım (her geliştirici kendi makinesinde bir defaya mahsus):

```bash
chmod +x scripts/onboard.sh
./scripts/onboard.sh
```

Bu komut `.githooks` içindeki hook'ları etkinleştirir ve post-commit işlemlerinin çalışmasını sağlar.

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

## Proje Yönetimi Modülü (Yeni)

Yaptığım eklemelerle `proje` adlı yeni bir Django uygulaması eklendi. Bu modül kentsel dönüşüm projelerini yönetmek için temel CRUD ve belge yönetimi işlevlerini sağlar.

- Uygulama: `proje`
- Modeller: `Project`, `Owner` (Malik), `Unit` (Bağımsız Bölüm), `Ownership`, `Agreement`, `Document`.
- URL alanı: `/proje/`
- Örnek yollar:
   - `/proje/` — Proje listesi
   - `/proje/add/` — Yeni proje ekle
   - `/proje/<pk>/` — Proje detay

Developer setup (linters)
-------------------------

To run Pylint with Django support locally, install the development requirements and use the repo `.pylintrc`:

```bash
python3 -m pip install -r requirements-dev.txt
pylint path/to/your/module.py
```

The `.pylintrc` in the repository enables the `pylint_django` plugin so Pylint will better understand Django model attributes (for example, `.objects`).

   - `/proje/<pk>/unit/add/` — Projeye bağımsız bölüm ekle
   - `/proje/<pk>/owner/add/` — Projeye malik ekle
   - `/proje/documents/` — Sistemdeki proje dosyaları

Kullanım notları:
- Uygulama Admin panelinden de yönetilebilir (`/admin/`).
- Dosya yükleme alanları `MEDIA` ayarlarınıza göre çalışacaktır; geliştirme için Django'nun `MEDIA_URL`/`MEDIA_ROOT` yapılandırmasını kullanabilirsiniz.

Test ve deploy:
- Yeni migration'lar oluşturuldu ve `python manage.py migrate` çalıştırıldı.
- Mevcut testler (`python manage.py test`) başarıyla geçti.

Gelecek adımlar (opsiyonel):
- Proje yetkilendirme (sadece proje staff/manager görüntüleyebilsin) ve granular izinler.
- Dosya önizleme (PDF/imagen thumbnail) ve doküman arama.
- Uzlaşma süreci için ayrıntılı durum izleme, bildirimler ve ilerleme göstergeleri.

- `HATALAR.md`: Tespit edilen hatalar ve çözümleri (çözülenleri işaretlenmiş).
- `TEMPLATES.md`: `templates/` dizinindeki önemli şablonların açıklamaları ve kullanımları.
- `TODO.md`: Bu zamana kadar oluşturduğum görev listesi ve durumları; ileride tamamlananları buradan güncelleyeceğim.

Dokümanlar repoda root dizininde yer almaktadır. Projeyi klonladıktan sonra bu dosyaları okuyarak yapılan işleri ve kalan görevleri hızlıca görebilirsiniz.

## Detaylı Kurulum & Deploy Rehberi

Aşağıdaki adımlar geliştirme ve üretim (deploy) için yaygın bir yol sağlar. Ortama özel ayarlarınız varsa uygun şekilde uyarlayın.

1) Yerel geliştirme ortamı (quickstart)

```bash
# proje köküne geçin
cd /path/to/Syncra-Crm-v2.0.0

# virtualenv oluşturup etkinleştir
python3 -m venv .venv
source .venv/bin/activate

# bağımlılıkları yükle
pip install --upgrade pip
pip install -r requirements.txt

# veritabanı migrate ve süper kullanıcı
python manage.py migrate
python manage.py createsuperuser

# statik dosyaları topla (geliştirme için opsiyonel)
python manage.py collectstatic --noinput

# geliştirme sunucusunu çalıştır
python manage.py runserver

# Tarayıcıda http://127.0.0.1:8000/ adresini açın
```

2) Sistem bağımlılıkları (WeasyPrint gibi native paketler gerekebilir)

Debian/Ubuntu örneği:

```bash
sudo apt update
sudo apt install -y build-essential libpango1.0-0 libcairo2 libgdk-pixbuf2.0-0 libffi-dev libxml2 libxslt1.1
```

3) Üretim için temel adımlar (Gunicorn + nginx örneği)

- Ortam değişkenlerini ayarlayın (`.env` veya systemd unit içinde): `DEBUG=False`, `SECRET_KEY`, `DATABASE_URL` veya DB ayrıntıları, `ALLOWED_HOSTS`.
- Sanal ortamı oluşturun ve bağımlılıkları yükleyin.
- Veritabanı migrate edin: `python manage.py migrate`.
- Statik dosyaları toplayın: `python manage.py collectstatic --noinput`.

Örnek systemd servis (gunicorn) — `/etc/systemd/system/syncra-gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon for Syncra CRM
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Syncra-Crm-v2.0.0
EnvironmentFile=/path/to/Syncra-Crm-v2.0.0/.env
ExecStart=/path/to/Syncra-Crm-v2.0.0/.venv/bin/gunicorn config.wsgi:application \
  --workers 3 --bind unix:/run/syncra.sock

[Install]
WantedBy=multi-user.target
```

Örnek nginx site konfigürasyonu (proxy to gunicorn):

```nginx
server {
   listen 80;
   server_name your.domain.com;

   location = /favicon.ico { access_log off; log_not_found off; }
   location /static/ {
      root /path/to/Syncra-Crm-v2.0.0/staticfiles;
   }

   location / {
      include proxy_params;
      proxy_pass http://unix:/run/syncra.sock;
   }
}
```

4) Güvenlik & performans ipuçları
- `DEBUG=False` yapın ve `ALLOWED_HOSTS`'ı ayarlayın.
- HTTPS kullanın (Let's Encrypt + certbot önerilir).
- Veritabanı bağlantı bilgilerini güvenli şekilde yönetin (`.env` veya secret manager).
- Statik ve medya dosyalarını CDN veya S3 benzeri servislerde saklamayı düşünün.

5) CI/CD notları
- Repo'da `.github/workflows/ci.yml` bulunur; push/pull requestlerde `collectstatic` ve testleri çalıştırır.

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
