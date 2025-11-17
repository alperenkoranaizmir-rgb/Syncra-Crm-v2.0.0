"""Create initial permission groups used by the `proje` app.

This migration creates two groups (`Proje Yöneticisi`,
`Kentsel Dönüşüm Uzmanı`) and assigns appropriate permissions for the
`proje` app models. The code is intentionally defensive: if ContentType
or Permission records are missing the migration will continue without
raising so migrations can run in partial environments.
"""
# pylint: disable=invalid-name,import-outside-toplevel

from django.db import migrations


def create_groups(apps, schema_editor):
    """Create the named groups and assign permissions for `proje` models.

    This function is defensive: missing content types or permissions are
    skipped so the migration does not fail when run in partial setups.
    """
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    # `schema_editor` is provided by Django but not used here
    del schema_editor

    # Models to assign permissions for
    model_names = ["owner", "unit", "agreement", "document"]

    # Create groups
    pg, _ = Group.objects.get_or_create(name="Proje Yöneticisi")
    ku, _ = Group.objects.get_or_create(name="Kentsel Dönüşüm Uzmanı")

    # Give Proje Yöneticisi add/change/delete on owner/unit/agreement/document
    for m in model_names:
        try:
            ct = ContentType.objects.get(app_label="proje", model=m)
        except ContentType.DoesNotExist:
            continue
        perms = Permission.objects.filter(content_type=ct)
        for p in perms:
            # assign all perms to proje yöneticisi
            pg.permissions.add(p)

    # Give Kentsel Dönüşüm Uzmanı add/change but NOT delete
    for m in model_names:
        try:
            ct = ContentType.objects.get(app_label="proje", model=m)
        except ContentType.DoesNotExist:
            continue
        add_codename = f"add_{m}"
        change_codename = f"change_{m}"
        for codename in (add_codename, change_codename):
            try:
                p = Permission.objects.get(content_type=ct, codename=codename)
                ku.permissions.add(p)
            except Permission.DoesNotExist:
                continue


def reverse_create_groups(apps, schema_editor):
    """Reverse operation: delete the created groups when rolling back.

    The function prefers to catch `DatabaseError` when deleting but will
    fall back silently if the exception class cannot be imported in the
    running environment.
    """
    Group = apps.get_model("auth", "Group")
    # `schema_editor` parameter is not used by this reverse function
    del schema_editor

    try:
        from django.db import DatabaseError  # type: ignore
    except ImportError:  # pragma: no cover - environment dependent
        # If DatabaseError cannot be imported, fall back to Exception so the
        # deletion attempt still runs but we do not fail the reversal due to
        # import issues in unusual environments.
        DatabaseError = Exception  # type: ignore

    try:
        Group.objects.filter(
            name__in=["Proje Yöneticisi", "Kentsel Dönüşüm Uzmanı"]
        ).delete()
    except DatabaseError:  # pylint: disable=broad-except
        # If DB is not available or in an unexpected state, ignore for reverse
        pass


class Migration(migrations.Migration):
    """Migration that creates initial groups and permissions for `proje`."""

    dependencies = [
        ("proje", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_create_groups),
    ]
