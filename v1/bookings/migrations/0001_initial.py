# Generated by Django 4.2.9 on 2024-03-06 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("services", "0006_serviceprovider_holidays"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Date Of Time Slot"
                    ),
                ),
                ("starting_time", models.TimeField()),
                ("ending_time", models.TimeField()),
                ("is_booked", models.BooleanField(default=False)),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="creator_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="services.serviceprovider",
                        verbose_name="Provider services",
                    ),
                ),
                (
                    "updater",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updater_%(class)s_objects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_on",),
                "abstract": False,
            },
        ),
    ]
