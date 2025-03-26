import functools
from typing import Optional

import requests
from loguru import logger

from agence.settings import KIWI_SEARCH_API_KEY, KIWI_API_URL
from app import models
from app.domain.entities.airport import Airport
from app.domain.repositories.airport_repository import IAirportRepository


class AirportRepository(IAirportRepository):
    _kiwi_api_key = KIWI_SEARCH_API_KEY

    # No need for LRU for now as we have little traffic
    @functools.cache
    def get_by_code(self, code: str) -> Airport:
        row = models.Airport.objects.filter(airport_code=code).first()

        if row:
            return Airport(
                code=row.airport_code,
                country_code=row.country_code,
                region_name=row.region_name,
                latitude=row.latitude,
                longitude=row.longitude,
                name=row.airport_name,
                icao=row.airport_code_icao
            )

        logger.warning(f"Unknown airport code {code}, trying to find it in Kiwi")

        airport_from_kiwi = self.__get_airport_from_kiwi(code)
        self.__add_to_db(airport_from_kiwi)

        if not airport_from_kiwi:
            logger.error(f"Unknown airport code: {code}")
            raise ValueError(f"Unknown airport code {code}")

        return airport_from_kiwi

    def __get_airport_from_kiwi(self, airport_code: str) -> Optional[Airport]:
        session = requests.Session()

        preprocessed_request = {
            'term': airport_code,
            'locale': 'en-US',
            'location_types': 'airport'
        }

        http_response = session.get(f"{KIWI_API_URL}/locations/query", params=preprocessed_request,
                                    headers={'apikey': self._kiwi_api_key})
        as_dict = http_response.json()

        airports = as_dict['locations']

        for airport in airports:
            if airport['code'] != airport_code:
                continue

            country = airport['city']['country']
            region = airport['city']['region']

            return Airport(
                code=airport_code,
                country_code=country['code'],
                region_name=region['name'],
                latitude=airport['location']['lat'],
                longitude=airport['location']['lon'],
                icao=airport['icao'],
                name=airport['name']
            )

        return None

    def __add_to_db(self, airport: Airport):
        models.Airport.objects.create(
            airport_name=airport.name,
            airport_code=airport.code,
            airport_code_icao=airport.icao,
            country_code=airport.country_code,
            region_name=airport.region_name,
            latitude=airport.latitude,
            longitude=airport.longitude
        )
