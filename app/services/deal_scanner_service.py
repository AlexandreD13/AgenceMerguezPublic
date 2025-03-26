import datetime
from functools import cache
from statistics import mean
from typing import List, Optional

from loguru import logger

from agence.settings import HISTORICAL_METRICS_MAX_TRIP_DURATION_IN_DAYS, HISTORICAL_METRICS_MIN_TRIP_DURATION_IN_DAYS, \
    HISTORICAL_METRICS_NUMBER_OF_DESTINATIONS_TO_SCAN, HISTORICAL_METRICS_DEAL_THRESHOLD_PERCENT, \
    HISTORICAL_METRICS_DEALS_SEARCH_THRESHOLD_PERCENT
from app.domain.entities.airport import Airport
from app.domain.entities.country import Country
from app.domain.entities.destination import Destination
from app.domain.entities.destination_type import DestinationType
from app.domain.entities.global_deals import GlobalDealsResponse
from app.domain.entities.subscription import SubscriptionWithDestinations
from app.domain.repositories.airport_repository import IAirportRepository
from app.domain.repositories.country_repository import ICountryRepository
from app.domain.repositories.deals_report_repository import IDealsReportRepository
from app.domain.repositories.destination_to_track_repository import IDestinationToTrackRepository
from app.domain.repositories.dto.get_destination_request import GetDestinationsRequest
from app.domain.repositories.monthly_historic_metric_repository import IMonthlyHistoricMetricRepository
from app.domain.repositories.subscriber_repository import ISubscriberRepository
from app.domain.repositories.subscription_repository import ISubscriptionRepository
from app.domain.services.deal_scanner_service import IDealScannerService
from app.domain.services.destination_service import IDestinationService
from app.domain.services.notifier_service import INotifierService


class DealScannerService(IDealScannerService):
    _destination_service: IDestinationService
    _notifier_service: INotifierService
    _subscriptions_repository: ISubscriptionRepository
    _subscriber_repository: ISubscriberRepository
    _destination_to_track_repository: IDestinationToTrackRepository
    _monthly_metrics_repository: IMonthlyHistoricMetricRepository
    _deals_report_repository: IDealsReportRepository
    _airport_repository: IAirportRepository
    _country_repository: ICountryRepository

    def __init__(self,
                 destination_service: IDestinationService,
                 notifier_service: INotifierService,
                 subscription_repository: ISubscriptionRepository,
                 subscriber_repository: ISubscriberRepository,
                 destination_to_track: IDestinationToTrackRepository,
                 monthly_metrics_repository: IMonthlyHistoricMetricRepository,
                 deals_report_repository: IDealsReportRepository,
                 airport_repository: IAirportRepository,
                 country_repository: ICountryRepository
                 ):
        self._destination_service = destination_service
        self._notifier_service = notifier_service
        self._subscriptions_repository = subscription_repository
        self._subscriber_repository = subscriber_repository
        self._destination_to_track_repository = destination_to_track
        self._monthly_metrics_repository = monthly_metrics_repository
        self._deals_report_repository = deals_report_repository
        self._airport_repository = airport_repository
        self._country_repository = country_repository

    def scan(self, subscriber_email: str, vip_only: Optional[bool]) -> List[SubscriptionWithDestinations]:
        subscriber = self._subscriber_repository.get_by_email(subscriber_email)

        if not subscriber:
            logger.warning(f"Undefined subscriber")
            return []

        subscriptions = self._subscriptions_repository.list_for_subscriber(subscriber, vip_only=vip_only)

        subscriptions_with_destinations: List[SubscriptionWithDestinations] = []

        for subscription in subscriptions.results:
            logger.info(f"Looking into {subscription}")
            req = GetDestinationsRequest.from_subscription(subscription)
            response = self._destination_service.fetch(req)

            subscriptions_with_destinations.append(SubscriptionWithDestinations(
                subscription, response.destinations
            ))

        return subscriptions_with_destinations

    def scan_global_deals(self) -> GlobalDealsResponse:
        logger.info(f"Scanning for global deals")

        destinations_to_track = self._destination_to_track_repository.get_all()
        deals: List[Destination] = []

        for d in destinations_to_track:
            origin_airport = self._airport_repository.get_by_code(d.origin_airport_code)
            logger.info(
                f"Looking for global deal from {origin_airport.code} to {d.destination_code} of type {d.destination_type}")

            monthly_historic = self._get_monthly_historic(origin_airport, d.destination_code, d.destination_type)
            monthly_average_prices = [m.average_price for m in monthly_historic]

            if not monthly_average_prices:
                logger.warning(
                    f"No monthly metrics for {d.destination_code}. You might want to refresh the monthly metrics.")
                continue

            destination_max_yearly_avg_price = max(monthly_average_prices)

            search_price_threshold = destination_max_yearly_avg_price * (
                1 - HISTORICAL_METRICS_DEALS_SEARCH_THRESHOLD_PERCENT
            )

            req = GetDestinationsRequest(
                currency_code='CAD',
                airport_code=origin_airport.code,
                max_budget=search_price_threshold,
                depart_date=datetime.date.today(),
                return_date=(datetime.datetime.now() + datetime.timedelta(days=360)).date(),
                trip_duration_range_in_days=(
                    HISTORICAL_METRICS_MIN_TRIP_DURATION_IN_DAYS,
                    HISTORICAL_METRICS_MAX_TRIP_DURATION_IN_DAYS
                ),
                destination=d.destination_code,
                destination_type=d.destination_type,
                limit=HISTORICAL_METRICS_NUMBER_OF_DESTINATIONS_TO_SCAN
            )

            response = self._destination_service.fetch(req)

            for destination in response.destinations:
                month = destination.depart_date.month

                average_price = self.__get_average_price(
                    origin_airport,
                    destination.destinationCountry,
                    destination.destinationAirport,
                    month
                )

                threshold_price = average_price * (1 - HISTORICAL_METRICS_DEAL_THRESHOLD_PERCENT)

                if destination.price < threshold_price:
                    deals.append(destination)

        logger.info(f"Done scanning global deals")

        logger.info(f"Storing results in the database")
        report_id = self._deals_report_repository.create(deals)
        logger.info(f"Done storing results")

        return GlobalDealsResponse(deals, report_id)

    @cache
    def __get_average_price(
        self,
        origin_airport: Airport,
        destination_country: Country,
        destination_airport: Airport,
        month: int
    ) -> float:
        country_monthly_metrics = self._monthly_metrics_repository.get_country_historic(origin_airport,
                                                                                        destination_country)
        country_metrics_by_month = {m.month_identifier: m for m in country_monthly_metrics}

        airport_monthly_metrics = self._monthly_metrics_repository.get_airport_historic(
            origin_airport,
            destination_airport
        )
        airport_metrics_by_month = {metric.month_identifier: metric for metric in airport_monthly_metrics}

        monthly_average_price = mean([m.average_price for m in country_monthly_metrics])

        if month in airport_metrics_by_month:
            monthly_average_price = airport_metrics_by_month.get(month).average_price
        elif len(airport_monthly_metrics) > 0:
            monthly_average_price = mean([metric.average_price for metric in airport_monthly_metrics])
        elif month in country_metrics_by_month:
            monthly_average_price = country_metrics_by_month.get(month).average_price

        return monthly_average_price

    def _get_monthly_historic(
        self,
        origin_airport: Airport,
        destination_code: str,
        destination_type: DestinationType
    ):
        if destination_type == DestinationType.COUNTRY:
            destination_country = self._country_repository.get_by_code(destination_code)
            return self._monthly_metrics_repository.get_country_historic(origin_airport, destination_country)
        elif destination_type == DestinationType.AIRPORT:
            destination_airport = self._airport_repository.get_by_code(destination_code)
            return self._monthly_metrics_repository.get_airport_historic(origin_airport, destination_airport)
        else:
            raise ValueError(f"unknown type: {destination_type}")
