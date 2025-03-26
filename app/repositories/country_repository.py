import functools
from typing import Optional

import requests
from loguru import logger

from agence.settings import KIWI_SEARCH_API_KEY, KIWI_API_URL
from app import models
from app.domain.entities.country import Country
from app.domain.repositories.country_repository import ICountryRepository


class CountryRepository(ICountryRepository):
    _kiwi_api_key = KIWI_SEARCH_API_KEY

    # We cache this method as loading the CSV in memory is quite expensive.
    # No need for LRU for now as we have little traffic
    @functools.cache
    def get_by_code(self, code: str) -> Optional[Country]:
        row = models.Country.objects.filter(country_code=code).first()

        if row:
            return Country(
                code=row.country_code,
                name=row.country_name,
                continent=row.continent_name,
                continent_code=row.continent_code
            )
        logger.warning(f"Unknown country code {code}, trying to find it in Kiwi")

        country_from_kiwi = self.__get_from_kiwi(code)
        self._add_to_db(country_from_kiwi)

        if not country_from_kiwi:
            logger.error(f"Unknown country code: {code}")

        return country_from_kiwi

    def __get_from_kiwi(self, country_code: str) -> Optional[Country]:
        session = requests.Session()

        preprocessed_request = {
            'term': country_code,
            'locale': 'en-US',
            'location_types': 'country'
        }

        http_response = session.get(f"{KIWI_API_URL}/locations/query", params=preprocessed_request,
                                    headers={'apikey': self._kiwi_api_key})
        as_dict = http_response.json()

        countries = as_dict['locations']

        for country in countries:
            if country['code'] != country_code:
                continue

            country_name = country['name']
            country_code = country['code']

            continent_name = country['continent']['name']
            continent_code = country['continent']['code']

            return Country(
                continent=continent_name,
                continent_code=continent_code,
                name=country_name,
                code=country_code,
            )

        return None

    def _add_to_db(self, country: Country):
        models.Country.objects.create(
            continent_name=country.continent,
            continent_code=country.continent_code,
            country_name=country.name,
            country_code=country.code,
        )
