# Yapılan İşler

Aşağıda bu çalışma sırasında repoya eklenen veya güncellenen önemli öğelerin kısa bir özeti bulunmaktadır.

- `config/` — Django proje ayarları, Türkçe locale ve SECRET_KEY yönetimi.
- `core/` — Demo sayfalarını sağlayan ana uygulama; `views`, `urls`, `tests` içerir.
- `templates/pages/` — AdminLTE demo sayfaları (charts, tables, calendar, gallery, mailbox, dashboard vb.).
- `static/css/` — Sayfa bazlı küçük stil override dosyaları eklendi: `charts_overrides.css`, `calendar_overrides.css`, `gallery_overrides.css`, `datatables_overrides.css`, `mailbox_overrides.css`.
- `scripts/` — Statik çakışma tespit ve template iyileştirme scriptleri (örnek: `list_static_conflicts.py`, `ensure_load_static.py`).
- `.github/workflows/ci.yml` — CI: collectstatic + test adımları.
- `.pre-commit-config.yaml` — Pre-commit hook'ları (black, isort, flake8, mypy, bandit) ve yerel test hook'u.

Detaylı yapılan değişiklikler commit geçmişinde bulunmaktadır; hızlı özet için bu dosyayı takip edebilirsiniz.
