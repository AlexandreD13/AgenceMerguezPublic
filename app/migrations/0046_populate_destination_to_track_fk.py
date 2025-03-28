# Generated by Django 4.2.2 on 2023-11-18 17:19

from django.db import migrations


def populate_columns(apps, schema_editor):
    Airport = apps.get_model('app', 'Airport')
    Country = apps.get_model('app', 'Country')
    DestinationToTrack = apps.get_model('app', 'DestinationToTrack')

    destinations = DestinationToTrack.objects.all()

    for d in destinations:
        t = d.destination_type
        d.origin_airport = Airport.objects.filter(airport_code=d.origin_airport_code).first()

        if t == 'AIRPORT':
            d.destination_airport = Airport.objects.filter(airport_code=d.destination_code).first()

        elif t == 'COUNTRY':
            d.destination_country = Country.objects.filter(country_code=d.destination_code).first()
        d.save()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0045_destinationtotrack_origin_airport'),
    ]

    operations = [
        migrations.RunPython(populate_columns),
    ]
