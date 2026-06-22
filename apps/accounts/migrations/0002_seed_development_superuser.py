# Generated for E-CON development bootstrap.

from __future__ import annotations

import os

from django.conf import settings
from django.db import migrations


def seed_development_superuser(apps, schema_editor):
    should_seed = (
        settings.DEBUG or os.getenv("DJANGO_SEED_DEV_SUPERUSER", "false").lower() == "true"
    )
    if not should_seed:
        return

    user_model = apps.get_model("accounts", "User")
    email = os.getenv("DJANGO_DEV_SUPERUSER_EMAIL", "admin@econ.local")
    password = os.getenv("DJANGO_DEV_SUPERUSER_PASSWORD", "ChangeMe123!")

    if user_model.objects.filter(email=email).exists():
        return

    user = user_model(
        email=email,
        first_name="Development",
        last_name="Admin",
        role="SUPER_ADMIN",
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    user.set_password(password)
    user.save(using=schema_editor.connection.alias)


def remove_development_superuser(apps, schema_editor):
    user_model = apps.get_model("accounts", "User")
    email = os.getenv("DJANGO_DEV_SUPERUSER_EMAIL", "admin@econ.local")
    user_model.objects.filter(email=email).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_development_superuser, remove_development_superuser),
    ]
