# Generated by Django 4.2.2 on 2023-11-18 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, related_name='subscriber2subscriptions', to='app.subscription'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscription2subscribers', to='app.subscriber'),
        ),
    ]
