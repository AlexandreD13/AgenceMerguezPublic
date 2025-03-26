from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import Optional, List

from dataclasses_json import dataclass_json

from app.domain.entities.airport import Airport
from app.domain.entities.country import Country


@dataclass_json
@dataclass
class DestinationCity:
    name: str
    code: Optional[str]


@dataclass_json
@dataclass
class Destination:
    depart_date: datetime.date
    return_date: datetime.date

    airlines: List[str]

    # todo: still needed? We could get the icon from the airline name None
    airlineIcon: Optional[str]

    originAirport: Airport
    originCountry: Country
    originCity: DestinationCity

    destinationAirport: Airport
    city: DestinationCity
    destinationCountry: Country
    tripDurationInDays: int
    flightDurationInHours: int
    price: float
    flightNumberOfStops: int
    clickoutUrl: Optional[str]

    def hash(self) -> str:
        args = ':'.join([
            str(self.tripDurationInDays),
            self.originAirport.code,
            self.depart_date.strftime("%Y-%m-%d"),
            self.return_date.strftime("%Y-%m-%d"),
            self.destinationAirport.code,
            self.city.name
        ]).encode('utf-8')
        return sha256(args).hexdigest()


@dataclass_json
@dataclass
class DestinationPartial:
    depart_date: datetime.date
    return_date: datetime.date

    airlines: List[str]

    # todo: still needed? We could get the icon from the airline name None
    airlineIcon: Optional[str]

    originAirportCode: str
    originCountryCode: str
    originCity: DestinationCity

    destinationAirportCode: str
    city: DestinationCity
    destinationCountryCode: str
    tripDurationInDays: int
    flightDurationInHours: int
    price: float
    flightNumberOfStops: int
    clickoutUrl: Optional[str]
