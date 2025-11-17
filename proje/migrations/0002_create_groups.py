from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

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
    Group = apps.get_model("auth", "Group")
    try:
        from django.db import DatabaseError

        try:
            Group.objects.filter(
                name__in=["Proje Yöneticisi", "Kentsel Dönüşüm Uzmanı"]
            ).delete()
        except DatabaseError:
            # If DB is not available or in an unexpected state, ignore for reverse
            pass
    except Exception:  # pylint: disable=broad-except
        # If we cannot import DatabaseError for some reason, silently ignore
        try:
            Group.objects.filter(
                name__in=["Proje Yöneticisi", "Kentsel Dönüşüm Uzmanı"]
            ).delete()
        except Exception:  # pylint: disable=broad-except
            pass


class Migration(migrations.Migration):

    dependencies = [
        ("proje", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_create_groups),
    ]
