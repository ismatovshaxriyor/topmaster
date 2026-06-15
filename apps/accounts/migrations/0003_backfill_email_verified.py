"""Grandfather existing accounts as email-verified.

Only sign-ups created after this migration go through the verification flow.
"""
from django.db import migrations


def mark_existing_verified(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.update(email_verified=True)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_email_verified"),
    ]

    operations = [
        migrations.RunPython(mark_existing_verified, migrations.RunPython.noop),
    ]
