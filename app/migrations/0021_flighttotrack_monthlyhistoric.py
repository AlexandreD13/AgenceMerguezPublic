# Generated by Django 4.2.2 on 2024-01-04 02:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0020_subscription_enabled_alter_subscription_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="FlightToTrack",
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
                ("depart", models.CharField(max_length=5)),
                ("destination", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="MonthlyHistoric",
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
                ("depart_airport", models.CharField(max_length=5)),
                ("destination_airport", models.CharField(max_length=5)),
                ("month_identifier", models.IntegerField()),
                ("minimum", models.IntegerField()),
                ("average", models.IntegerField()),
                ("maximum", models.IntegerField()),
                ("last_refresh_datetime", models.DateTimeField()),
            ],
        ),
    ]
