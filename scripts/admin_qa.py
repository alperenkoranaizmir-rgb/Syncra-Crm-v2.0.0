"""Admin visual QA helper.

Creates a superuser if missing, logs in using Django's test Client,
fetches the admin add form for `proje.document` and writes an HTML snapshot
to `scripts/admin_add_snapshot.html` for offline review.

Run with:

```bash
DJANGO_SETTINGS_MODULE=config.settings python3 scripts/admin_qa.py
```

Note: This requires Django and project dependencies installed in the
active Python environment.
"""

import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

try:
    import django
    django.setup()
except Exception as exc:  # pragma: no cover - environment dependent
    print("Django not available or failed to setup:", exc, file=sys.stderr)
    sys.exit(2)

from django.contrib.auth import get_user_model
from django.test.client import Client

OUT_FILE = os.path.join(os.path.dirname(__file__), "admin_add_snapshot.html")


def ensure_superuser(username="admin", email="admin@example.com", password="admin123"):
    """Create or update a superuser with given credentials.

    Returns the (username, password) tuple used to login.
    """
    User = get_user_model()
    user, created = User.objects.get_or_create(username=username, defaults={"email": email, "is_superuser": True, "is_staff": True})
    if not created:
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
    else:
        user.set_password(password)
        user.save()
    return username, password


def fetch_admin_add_snapshot(url_path="/admin/proje/document/add/"):
    username, password = ensure_superuser()
    client = Client()
    logged_in = client.login(username=username, password=password)
    if not logged_in:
        print("Failed to login as superuser; check credentials or DB.")
        return False
    response = client.get(url_path)
    if response.status_code != 200:
        print(f"Admin page returned status {response.status_code}")
        return False
    with open(OUT_FILE, "wb") as fh:
        fh.write(response.content)
    print(f"Saved admin snapshot to {OUT_FILE}")
    return True


if __name__ == "__main__":
    fetch_admin_add_snapshot()
