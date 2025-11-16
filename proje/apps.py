from django.apps import AppConfig


class ProjeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "proje"
    verbose_name = "Proje Yönetimi"

    def ready(self):
        # Ensure groups exist when app is ready
        from django.contrib.auth.models import Group

        try:
            Group.objects.get_or_create(name="Proje Yöneticisi")
            Group.objects.get_or_create(name="Kentsel Dönüşüm Uzmanı")
        except Exception:
            # ready may run before migrations during initial setup; ignore errors
            pass
