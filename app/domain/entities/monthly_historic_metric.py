from dataclasses import dataclass

from datetime import datetime

from app.domain.entities.airport import Airport
from app.domain.entities.country import Country


@dataclass
class MonthlyHistoricMetricForAirport:
    depart_airport: str
    destination_airport: str

    # 1-based month identifier
    month_identifier: int

    # Monthly metrics
    minimum_price: int
    average_price: int
    maximum_price: int
    number_of_datapoints: int

    # Last refresh datetime
    last_refresh_datetime: datetime

@dataclass
class MonthlyHistoricMetricForCountry:
    origin: Airport
    destination: Country

    # 1-based month identifier
    month_identifier: int

    # Monthly metrics
    minimum_price: int
    average_price: int
    maximum_price: int
    number_of_datapoints: int

    # Last refresh datetime
    last_refresh_datetime: datetime
