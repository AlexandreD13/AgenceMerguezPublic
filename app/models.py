import uuid

from django.core.exceptions import ValidationError
from django.db import models


class Currency(models.TextChoices):
    CAD = 'CAD', 'Canadian Dollar'
    USD = 'USD', 'US Dollar'


class DestinationType(models.TextChoices):
    AIRPORT = 'AIRPORT', 'Airport'
    COUNTRY = 'COUNTRY', 'Country'


class Airport(models.Model):
    airport_name = models.CharField(max_length=100, blank=False)
    airport_code = models.CharField(max_length=5, blank=False, unique=True)
    airport_code_icao = models.CharField(max_length=5, blank=False)
    country_code = models.CharField(max_length=5, blank=False)
    region_name = models.CharField(max_length=100, blank=False)

    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)

    def __str__(self):
        return "{} - {} ({})".format(self.airport_code, self.airport_name, self.country_code)


class Country(models.Model):
    continent_name = models.CharField(max_length=50, blank=False)
    continent_code = models.CharField(max_length=5, blank=False)

    country_name = models.CharField(max_length=100, blank=False)
    country_code = models.CharField(max_length=5, blank=False, unique=True)

    def __str__(self):
        return "{} - {} ({})".format(self.country_code, self.country_name, self.continent_name)


class Subscription(models.Model):
    subscribers = models.ManyToManyField('Subscriber', through='SubscriptionsToSubscribers', blank=True)

    depart_airport = models.CharField(max_length=5, blank=False)

    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True, blank=True)
    destination_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    max_budget = models.IntegerField(blank=True)
    vip = models.BooleanField(default=False)

    description = models.CharField(max_length=50, null=True, blank=True)

    # Optional as it will fall back on the subscriber currency
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        blank=True
    )

    depart_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    exact_dates = models.BooleanField(blank=True, default=False)

    flight_max_duration_in_hours = models.IntegerField(blank=True, null=True)

    trip_duration_in_days_min = models.IntegerField(blank=True, null=True, default=7)
    trip_duration_in_days_max = models.IntegerField(blank=True, null=True, default=14)

    flight_max_stops = models.IntegerField(blank=True, null=True)

    enabled = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.destination_country and self.destination_airport:
            raise ValidationError(f"Either the country or the airport can be defined, not both")

        if self.destination_country is None and self.destination_airport is None:
            raise ValidationError(f"You must at least select an destination airport or destination country")

        super().save(*args, **kwargs)

    def __str__(self):
        if self.description:
            return self.description

        names = [s.email for s in self.subscribers.all()]

        return f"{self.destination} for {', '.join(names)}"


class Subscriber(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email: str = models.CharField(max_length=50, blank=False, unique=True)
    preferred_airport = models.CharField(max_length=5, blank=True)

    subscriptions = models.ManyToManyField('Subscription', through='SubscriptionsToSubscribers', blank=True)

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.CAD
    )

    subscribe_to_generic_deals = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class FeatureFlag(models.Model):
    name = models.CharField(max_length=50, blank=False)
    enabled = models.BooleanField(default=False)
    user = models.ForeignKey(Subscriber, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name='name_user_unique_constraint')
        ]

    def __str__(self):
        return f"{self.name} ({self.user}): {self.enabled}"


class SubscriptionsToSubscribers(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    def __str__(self):
        return "{}_{}".format(self.subscriber.__str__(), self.subscription.__str__())


class MonthlyHistoric(models.Model):
    depart_airport = models.CharField(max_length=5, blank=False)
    depart_country_code = models.CharField(max_length=5)

    destination_airport = models.CharField(max_length=5, blank=False)
    destination_country_code = models.CharField(max_length=5)

    month_identifier = models.IntegerField(blank=False)

    minimum_price = models.IntegerField(blank=False)
    average_price = models.IntegerField(blank=False)
    maximum_price = models.IntegerField(blank=False)
    number_of_datapoints = models.BigIntegerField(blank=False, default=0)
    last_refresh_datetime = models.DateTimeField(blank=False)

    def __str__(self):
        return "{}_{}_{}".format(self.depart_airport, self.destination_airport, self.month_identifier)


class DestinationToTrack(models.Model):
    origin_airport = models.ForeignKey(Airport, on_delete=models.CASCADE,
                                       related_name='destination_to_track_origin_airport')

    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True)
    destination_country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['origin_airport', 'destination_airport', 'destination_country'],
                                    name='airport_country_unique_constraint')
        ]

    def save(self, *args, **kwargs):
        if self.destination_country and self.destination_airport:
            raise ValidationError(f"Either the country or the airport can be defined, not both")


        if self.destination_country is None and self.destination_airport is None:
            raise ValidationError(f"You must at least select an destination airport or destination country")

        super().save(*args, **kwargs)

    def __str__(self):
        if self.destination_country is not None:
            return "{} --> {} (C)".format(
                self.origin_airport.airport_code,
                self.destination_country.country_code,
            )
        else:
            return "{} --> {} (A)".format(
                self.origin_airport.airport_code,
                self.destination_airport.airport_code
            )


class DealsReporting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(blank=False, auto_now_add=True)
    deals_json = models.JSONField(blank=False)
