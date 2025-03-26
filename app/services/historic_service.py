import datetime
from statistics import mean
from typing import List, Dict

from django.utils import timezone
from loguru import logger

from agence.settings import HISTORICAL_METRICS_MIN_TRIP_DURATION_IN_DAYS, HISTORICAL_METRICS_MAX_TRIP_DURATION_IN_DAYS, \
    HISTORICAL_METRICS_NUMBER_OF_MONTHS_IN_FUTURE_TO_SCAN, \
    HISTORICAL_METRICS_NUMBER_OF_MONTHS_IN_FUTURE_TO_SCAN_WHEN_NOT_INITIALIZED, \
    HISTORICAL_METRICS_NUMBER_OF_DESTINATIONS_TO_SCAN
from app.domain.entities.airport import Airport
from app.domain.entities.destination import Destination
from app.domain.entities.destination_type import DestinationType
from app.domain.entities.monthly_historic_metric import MonthlyHistoricMetricForAirport
from app.domain.repositories.airport_repository import IAirportRepository
from app.domain.repositories.country_repository import ICountryRepository
from app.domain.repositories.destination_to_track_repository import IDestinationToTrackRepository
from app.domain.repositories.dto.get_destination_request import GetDestinationsRequest
from app.domain.repositories.monthly_historic_metric_repository import IMonthlyHistoricMetricRepository
from app.domain.services.destination_service import IDestinationService
from app.domain.services.historic_service import IHistoricService


class HistoricService(IHistoricService):
    _destinations: IDestinationService
    _destination_to_track_repo: IDestinationToTrackRepository
    _monthly_metric: IMonthlyHistoricMetricRepository
    _airport_repository: IAirportRepository
    _country_repository: ICountryRepository

    def __init__(
        self,
        destination_service: IDestinationService,
        destination_to_track_repository: IDestinationToTrackRepository,
        monthly_historic_metric_repository: IMonthlyHistoricMetricRepository,
        airport_repository: IAirportRepository,
        country_repository: ICountryRepository
    ):
        self._destinations = destination_service
        self._destination_to_track_repo = destination_to_track_repository
        self._monthly_metric = monthly_historic_metric_repository
        self._airport_repository = airport_repository
        self._country_repository = country_repository

    def refresh_monthly_metrics(
        self,
        origin_airport: Airport,
        destination_code: str,
        destination_type: DestinationType
    ):
        # Request an extra month to be able to get the end range.
        months_to_scan = self.__get_months_to_scan(
            HISTORICAL_METRICS_NUMBER_OF_MONTHS_IN_FUTURE_TO_SCAN_WHEN_NOT_INITIALIZED + 1
        )

        for i in range(len(months_to_scan) - 1):
            depart_date = months_to_scan[i]
            return_date = months_to_scan[i + 1]

            month_identifier = depart_date.month

            metric_for_destination = self._get_metric_for_destination(
                origin_airport,
                destination_code,
                destination_type,
                month_identifier
            )

            if metric_for_destination is not None and i >= HISTORICAL_METRICS_NUMBER_OF_MONTHS_IN_FUTURE_TO_SCAN:
                # The metrics are already initialized and we can stop refreshing.
                break

            airport_code = origin_airport.code

            fetch_request = GetDestinationsRequest(
                currency_code='CAD',
                airport_code=airport_code,
                depart_date=depart_date,
                return_date=return_date,
                trip_duration_range_in_days=(
                    HISTORICAL_METRICS_MIN_TRIP_DURATION_IN_DAYS,
                    HISTORICAL_METRICS_MAX_TRIP_DURATION_IN_DAYS
                ),
                destination=destination_code,
                destination_type=destination_type,
                limit=HISTORICAL_METRICS_NUMBER_OF_DESTINATIONS_TO_SCAN
            )

            response = self._destinations.fetch(fetch_request)

            destinations_by_airport = self.__group_destinations_by_destination_airport(response.destinations)

            for airport_code, destinations in destinations_by_airport.items():
                destination_airport = self._airport_repository.get_by_code(airport_code)
                monthly_metric = self._monthly_metric.get_airport_historic_for_month(
                    origin_airport,
                    destination_airport,
                    destinations[0].depart_date.month
                )

                if not monthly_metric:
                    monthly_metric = MonthlyHistoricMetricForAirport(
                        depart_airport=origin_airport.code,
                        destination_airport=destination_airport.code,
                        month_identifier=month_identifier,
                        minimum_price=999999,
                        average_price=-1,
                        maximum_price=-1,
                        number_of_datapoints=0,
                        last_refresh_datetime=timezone.now()
                    )

                # Update the min/max/average values from the response data
                monthly_prices = [destination.price for destination in destinations]

                if not monthly_prices:
                    continue

                monthly_metric.minimum_price = min(monthly_prices + [monthly_metric.minimum_price])
                monthly_metric.maximum_price = max(monthly_prices + [monthly_metric.maximum_price])
                monthly_metric.number_of_datapoints += len(monthly_prices)

                if monthly_metric.average_price == -1:
                    monthly_metric.average_price = mean(monthly_prices)
                else:
                    monthly_metric.average_price = mean(monthly_prices + [monthly_metric.average_price])

                # Upsert the row
                logger.info(
                    f"Updating monthly metric for: {origin_airport.code} -> {destination_airport.code}."
                    + f"Price[min: {monthly_metric.minimum_price}, avg: {monthly_metric.average_price}, max: {monthly_metric.maximum_price}"
                )
                self._monthly_metric.upsert(monthly_metric, origin_airport, destination_airport)

    def __group_destinations_by_destination_airport(
        self,
        destinations: List[Destination]
    ) -> Dict[str, List[Destination]]:
        acc: Dict[str, List[Destination]] = {}

        for d in destinations:
            if d.destinationAirport.code not in acc:
                acc[d.destinationAirport.code] = []
            acc[d.destinationAirport.code].append(d)

        return acc

    def __get_months_to_scan(self, number_of_future_months_to_scan: int) -> List[datetime.date]:
        months: List[datetime.date] = []

        current_month = datetime.datetime.today().month
        current_year = datetime.datetime.today().year

        for i in range(1, number_of_future_months_to_scan + 1):
            year_offset = (current_month + i - 1) // 12

            month = (current_month + i - 1) % 12 + 1
            year = current_year + year_offset

            months.append(datetime.date(year, month, 1))

        return months

    def _get_metric_for_destination(
        self,
        origin_airport: Airport,
        destination_code: str,
        destination_type: DestinationType,
        month_identifier: int
    ):

        if destination_type == DestinationType.COUNTRY:
            country = self._country_repository.get_by_code(destination_code)
            return self._monthly_metric.get_country_historic_for_month(origin_airport, country, month_identifier)
        elif destination_type == DestinationType.AIRPORT:
            airport = self._airport_repository.get_by_code(destination_code)
            return self._monthly_metric.get_airport_historic_for_month(origin_airport, airport, month_identifier)
        else:
            raise ValueError("not expected")
