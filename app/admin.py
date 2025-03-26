# Register your models here.
from django.contrib import admin

from .models import Subscriber, Subscription, SubscriptionsToSubscribers, \
    MonthlyHistoric, FeatureFlag, DestinationToTrack, Country, Airport


class SubscriptionInline(admin.TabularInline):
    model = Subscriber.subscriptions.through
    extra = 1


class SubscriberAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline]


class SubscriberInline(admin.TabularInline):
    model = Subscription.subscribers.through
    extra = 1


class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriberInline]
    autocomplete_fields = ['destination_airport', 'destination_country']


class AirportAdmin(admin.ModelAdmin):
    ordering = ['airport_code']
    search_fields = ['airport_code', 'airport_name']


class CountryAdmin(admin.ModelAdmin):
    ordering = ['country_code']
    search_fields = ['country_code', 'country_name']

class DestinationToTrackAdmin(admin.ModelAdmin):
    autocomplete_fields = ['origin_airport','destination_airport', 'destination_country']


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(SubscriptionsToSubscribers)
admin.site.register(MonthlyHistoric)
admin.site.register(FeatureFlag)
admin.site.register(DestinationToTrack,DestinationToTrackAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Airport, AirportAdmin)
