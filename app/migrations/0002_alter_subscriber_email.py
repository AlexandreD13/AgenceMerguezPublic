# Generated by Django 4.2.2 on 2023-10-19 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
