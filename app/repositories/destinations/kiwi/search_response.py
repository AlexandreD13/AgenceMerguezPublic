import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json, config

from app.domain.entities.destination import DestinationCity, DestinationPartial
from app.domain.repositories.dto.get_destination_response import GetDestinationResponsePartial
from app.utils import date_encoder


@dataclass_json
@dataclass
class ItineraryRoute:
    airline: str
    # IATA code identifier of the destination airport.
    flyTo: str

    # IATA code identifier of the origin airport.
    flyFrom: str

    # The name of the city of origin in the requested language (locale). In case of emergency, fallback to English.
    cityFrom: str

    # The name of the destination city in the requested language (locale). In case of emergency, fallback to English.
    cityTo: str

    # Represents city code of departure city. If it does not have a city code it can be null.
    cityCodeFrom: Optional[str]

    # Represents city code of arrival city. If it does not have a city code it can be null.
    cityCodeTo: Optional[str]

    utc_arrival: datetime.datetime = field(
        metadata=config(
            encoder=date_encoder.datetime_to_str,
            decoder=date_encoder.str_to_datetime,
        )
    )

    utc_departure: datetime.datetime = field(
        metadata=config(
            encoder=date_encoder.datetime_to_str,
            decoder=date_encoder.str_to_datetime,
        )
    )


@dataclass_json
@dataclass
class ItineraryCountry:
    code: str
    name: str


@dataclass_json
@dataclass
class ItineraryDuration:
    departure: int
    arrival: int = field(
        metadata=config(
            field_name='return',
        )
    )
    total: int


@dataclass_json
@dataclass
class Itineraries:
    airlines: List[str]
    booking_token: str
    countryFrom: ItineraryCountry
    countryTo: ItineraryCountry

    # Affiliate link
    deep_link: str

    # The hops of the itinerary
    route: List[ItineraryRoute]

    has_airport_change: bool

    price: float

    # IATA code identifier of the destination airport.
    flyTo: str

    # IATA code identifier of the origin airport.
    flyFrom: str

    # The name of the city of origin in the requested language (locale). In case of emergency, fallback to English.
    cityFrom: str

    # The name of the destination city in the requested language (locale). In case of emergency, fallback to English.
    cityTo: str

    # Represents city code of departure city. If it does not have a city code it can be null.
    cityCodeFrom: Optional[str]

    # Represents city code of arrival city. If it does not have a city code it can be null.
    cityCodeTo: Optional[str]

    duration: ItineraryDuration

    # Number of technical stops. It is visible from route represented as well by 2 segments with the same flight number.
    technical_stops: int

    utc_arrival: datetime.datetime = field(
        metadata=config(
            field_name='utc_arrival',
            encoder=date_encoder.datetime_to_str,
            decoder=date_encoder.str_to_datetime,
        )
    )

    utc_departure: datetime.datetime = field(
        metadata=config(
            field_name='utc_departure',
            encoder=date_encoder.datetime_to_str,
            decoder=date_encoder.str_to_datetime,
        )
    )

    def to_domain(self) -> DestinationPartial:
        return DestinationPartial(
            depart_date=self.route[0].utc_departure.date(),
            return_date=self.route[-1].utc_arrival.date(),
            airlines=self.airlines,
            airlineIcon=None,
            originCity=DestinationCity(
                name=self.cityFrom,
                code=self.cityCodeFrom
            ),
            originAirportCode=self.flyFrom,
            originCountryCode=self.countryFrom.code,
            destinationAirportCode=self.flyTo,
            city=DestinationCity(
                name=self.cityTo,
                code=self.cityCodeTo,
            ),
            destinationCountryCode=self.countryTo.code,
            tripDurationInDays=(self.utc_arrival - self.utc_departure).days,

            flightDurationInHours=self.duration.total / 3600.0,
            price=self.price,

            flightNumberOfStops=self.technical_stops,
            clickoutUrl=self.deep_link
        )


@dataclass_json
@dataclass
class SearchResponse:
    data: List[Itineraries]

    def to_domain(self) -> GetDestinationResponsePartial:
        return GetDestinationResponsePartial(
            destinations=[d.to_domain() for d in self.data]
        )
