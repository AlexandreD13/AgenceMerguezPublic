# Generated by Django 4.2.2 on 2024-01-29 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_remove_subscription_destination_coordinate_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DestinationCoordinate',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='destination_type',
            field=models.CharField(choices=[('AIRPORT', 'Airport'), ('COUNTRY', 'Country')], default='COUNTRY'),
        ),
    ]
