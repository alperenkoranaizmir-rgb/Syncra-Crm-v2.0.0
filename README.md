# Syncra CRM v2.0.0

Kısa açıklama
- Syncra CRM: Kurumsal müşteri ilişkileri yönetimi (CRM) uygulamasının Django tabanlı sürümü.

Önemli not
- Bu proje yerel geliştirme ve dağıtım amaçlıdır. Aşağıdaki komutlar ve adımlar tipik bir Django projesi için genel rehberdir; projeye özgü ek yapılandırmalar `settings`, `.env` veya `deployment` dokümanlarında bulunabilir.

Gereksinimler
- Python 3.8+ (sanal ortam önerilir)
- `pip`
- (Opsiyonel) `virtualenv` veya `venv`

Hızlı kurulum
1. Depoyu klonlayın veya proje dizinine geçin:

   ```bash
   cd /path/to/Syncra-Crm-v2.0.0
   ```

2. Sanal ortam oluşturun ve etkinleştirin:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
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
