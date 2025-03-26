from typing import List

from app.domain.entities.destination import Destination
from app.domain.repositories.airport_repository import IAirportRepository
from app.domain.repositories.country_repository import ICountryRepository
from app.domain.repositories.destination_repository import IDestinationRepository
from app.domain.repositories.dto.get_destination_request import GetDestinationsRequest
from app.domain.repositories.dto.get_destination_response import GetDestinationResponse
from app.domain.services.destination_service import IDestinationService


class DestinationService(IDestinationService):
    _destination_repository: IDestinationRepository
    _country_repository: ICountryRepository
    _airport_repository: IAirportRepository

    def __init__(
        self,
        destination_repository: IDestinationRepository,
        country_repository: ICountryRepository,
        airport_repository: IAirportRepository
    ):
        self._destination_repository = destination_repository
        self._country_repository = country_repository
        self._airport_repository = airport_repository

    def fetch(self, request: GetDestinationsRequest) -> GetDestinationResponse:
        response = self._destination_repository.fetch(request)

        partial_destinations = response.destinations

        destinations: List[Destination] = []

        for d in partial_destinations:
            origin_country = self._country_repository.get_by_code(d.originCountryCode)
            origin_airport = self._airport_repository.get_by_code(d.originAirportCode)

            destination_country = self._country_repository.get_by_code(d.destinationCountryCode)
            destination_airport = self._airport_repository.get_by_code(d.destinationAirportCode)

            new_destination = Destination(
                depart_date=d.depart_date,
                return_date=d.return_date,

                airlines=d.airlines,
                airlineIcon=d.airlineIcon,
                originAirport=origin_airport,
                originCountry=origin_country,
                originCity=d.originCity,

                destinationAirport=destination_airport,
                destinationCountry=destination_country,
                city=d.city,
                tripDurationInDays=d.tripDurationInDays,
                flightDurationInHours=d.flightDurationInHours,
                price=d.price,
                flightNumberOfStops=d.flightNumberOfStops,
                clickoutUrl=d.clickoutUrl
            )

            destinations.append(new_destination)

        return GetDestinationResponse(destinations)
