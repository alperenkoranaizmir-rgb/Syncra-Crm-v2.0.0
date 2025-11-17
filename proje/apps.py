from django.apps import AppConfig


class ProjeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proje"
    verbose_name = "Proje Yönetimi"

    def ready(self):
        # Ensure groups exist when app is ready
        from django.contrib.auth.models import Group
        try:
            from django.db.utils import OperationalError, ProgrammingError
        except Exception:  # pylint: disable=broad-except
            # If we cannot import DB exceptions, attempt to create groups but
            # guard broadly (this is a very early-import environment).
            try:
                Group.objects.get_or_create(name="Proje Yöneticisi")
                Group.objects.get_or_create(name="Kentsel Dönüşüm Uzmanı")
            except Exception:  # pylint: disable=broad-except
                pass
        else:
            try:
                Group.objects.get_or_create(name="Proje Yöneticisi")
                Group.objects.get_or_create(name="Kentsel Dönüşüm Uzmanı")
            except (OperationalError, ProgrammingError, ImportError):
                # safe to ignore during initial app import
                pass
