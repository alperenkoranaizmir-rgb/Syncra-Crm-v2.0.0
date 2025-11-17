"""Signal handlers for accounts app.

- create Profile when a User is created
- sync User.is_active when Profile.is_active_employee changes
"""
import logging

from django.db import DatabaseError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create empty Profile when a new User is created.

    This is best-effort: database errors are logged at debug level and
    not re-raised to avoid breaking user creation flows.
    """
    # Mark sender as used to satisfy linters (we don't need it otherwise)
    _ = sender

    if created:
        try:
            Profile.objects.create(user=instance)
        except DatabaseError:
            logging.getLogger(__name__).debug(
                "Could not create Profile for user %r", instance
            )


@receiver(pre_save, sender=Profile)
def sync_user_active(sender, instance, **kwargs):
    """Ensure `User.is_active` follows `Profile.is_active_employee`.

    If the Profile previously existed and the active flag changed, update
    the related User. Database errors are handled narrowly and logged.
    """
    # Use sender variable to satisfy linters even though it is unused.
    _ = sender

    if instance.pk:
        try:
            old = Profile.objects.get(pk=instance.pk)
        except Profile.DoesNotExist:
            old = None

        if old and old.is_active_employee != instance.is_active_employee:
            instance.user.is_active = instance.is_active_employee
            try:
                instance.user.save(update_fields=["is_active"])
            except DatabaseError:
                logging.getLogger(__name__).debug(
                    "Could not update is_active for user %r", instance.user
                )
    else:
        # New profile: set user active according to the profile flag.
        instance.user.is_active = instance.is_active_employee
        try:
            instance.user.save(update_fields=["is_active"])
        except DatabaseError:
            logging.getLogger(__name__).debug(
                "Could not set is_active for new user %r", instance.user
            )
