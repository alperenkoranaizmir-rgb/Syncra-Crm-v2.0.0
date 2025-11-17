"""App configuration for the `accounts` application.

Registers signal handlers during app startup. Import failures are
logged at debug level rather than re-raised to avoid breaking
management commands or migrations when signals are not required.
"""

import importlib
import logging

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Django AppConfig for `accounts`.

    The `ready` hook imports the module containing signal registrations.
    If that import fails because the module is absent (e.g. during some
    management operations), we log the condition at debug level instead
    of raising an exception.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "Kullanıcı Yönetimi"

    def ready(self):
        # Import signals to register handlers. Use importlib so pylint does
        # not warn about an import-outside-toplevel. Only handle ImportError.
        try:
            importlib.import_module(f"{self.name}.signals")
        except ImportError:
            logging.getLogger(__name__).debug("accounts.signals not available")
