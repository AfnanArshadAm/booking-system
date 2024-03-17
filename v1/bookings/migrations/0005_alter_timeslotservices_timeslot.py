# Generated by Django 4.2.9 on 2024-03-16 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0004_timeslotservices"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timeslotservices",
            name="timeslot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="timeslotservices",
                to="bookings.timeslot",
                verbose_name="Timeslot",
            ),
        ),
    ]
