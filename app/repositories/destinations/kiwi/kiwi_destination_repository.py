import datetime
import functools
import logging
from typing import Optional

import requests

from agence.settings import KIWI_API_URL
from app.domain.entities.destination_type import DestinationType
from app.domain.repositories.destination_repository import IDestinationRepository
from app.domain.repositories.dto.get_destination_request import GetDestinationsRequest
from app.domain.repositories.dto.get_destination_response import GetDestinationResponsePartial
from app.repositories.destinations.kiwi.search_response import SearchResponse
from app.utils import optional, date_encoder

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class KiwiDestinationRepository(IDestinationRepository):
    _api_key: str

    def __init__(self, api_key: str):
        if not api_key:
            raise Exception("API Key was not provided")

        self._api_key = api_key

    def fetch(self, request: GetDestinationsRequest) -> GetDestinationResponsePartial:
        session = requests.Session()

        preprocessed_request = self.__build_fetch_request(request)

        http_response = session.get(f"{KIWI_API_URL}/v2/search", params=preprocessed_request,
                                    headers={'apikey': self._api_key})

        r: SearchResponse = SearchResponse.from_dict(http_response.json())

        return r.to_domain()

    @functools.cache
    def __get_location_code(self, destination: str, destination_type: DestinationType) -> Optional[str]:
        session = requests.Session()

        preprocessed_request = {
            'term': destination,
            'locale': 'en-US',
            'location_types': 'airport' if destination_type == DestinationType.AIRPORT else 'country'
        }

        http_response = session.get(f"{KIWI_API_URL}/locations/query", params=preprocessed_request,
                                    headers={'apikey': self._api_key})
        as_dict = http_response.json()

        if as_dict['locations']:
            return as_dict['locations'][0]['code']

        return None

    def __build_fetch_request(self, request: GetDestinationsRequest) -> dict:
        r = request

        depart_date = r.depart_date or datetime.date.today()
        return_date = r.return_date or (depart_date + datetime.timedelta(days=180))

        fly_to = None

        if r.destination and r.destination_type:
            fly_to = self.__get_location_code(r.destination, r.destination_type)

        json_request = {
            'fly_from': f'airport:{r.airport_code}',
            'fly_to': fly_to,

            'curr': r.currency_code,
            'price_to': optional.map(r.max_budget, int),

            # max number of stopovers per the entire itinerary (outbound + return).
            'max_stopovers': optional.map(r.flight_max_stops, lambda x: x * 2),

            'vehicle_type': 'aircraft',
            'locale': 'ca-fr',

            # max itinerary duration in hours, min value 0
            'max_fly_duration': r.max_flight_duration_in_hours,

            # dd/mm/yyyy
            'date_from': date_encoder.date_to_day_month_year(depart_date),
            'date_to': date_encoder.date_to_day_month_year(
                depart_date if r.exact_dates else return_date
            ),

            'return_to': date_encoder.date_to_day_month_year(return_date),
            'return_from': date_encoder.date_to_day_month_year(return_date if r.exact_dates else depart_date),

            # the minimal length of stay in the destination given in the fly_to
            'nights_in_dst_from': optional.map(r.trip_duration_range_in_days, lambda xy: {xy[0]}),
            # the maximal length of stay in the destination given in the fly_to parameter.
            'nights_in_dst_to': optional.map(r.trip_duration_range_in_days, lambda xy: {xy[1]}),

            # limit number of results; the default value is 200; max is 1000
            'limit': r.limit,
            'sort': 'price'
        }

        return json_request


if __name__ == "__main__":
    repo = KiwiDestinationRepository('replaceMe')
    response = repo.fetch(
        GetDestinationsRequest(airport_code="YUL", currency_code='CAD', depart_date=datetime.date(2024, 2, 1)))
    print(response)
