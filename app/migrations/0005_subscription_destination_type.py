# Generated by Django 4.2.2 on 2023-11-02 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_subscription_depart_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='destination_type',
            field=models.CharField(choices=[('AIRPORT', 'Airport'), ('FREE_TEXT', 'Free text search')], default='FREE_TEXT'),
        ),
    ]
