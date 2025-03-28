# Generated by Django 4.2.2 on 2024-02-19 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_subscription_destination_airport_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='destination_type',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='destination_airport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.airport'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='destination_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.country'),
        ),
    ]
