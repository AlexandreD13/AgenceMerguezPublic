import dataclasses
import datetime
from typing import Optional, Tuple

from app.domain.entities.destination_type import DestinationType
from app.domain.entities.subscription import Subscription


@dataclasses.dataclass
class GetDestinationsRequest:
    currency_code: str
    airport_code: Optional[str] = None

    max_budget: Optional[float] = None

    depart_date: Optional[datetime.date] = None
    return_date: Optional[datetime.date] = None
    exact_dates: Optional[bool] = None

    # 3 to 4 days -> (3,4)
    trip_duration_range_in_days: Optional[Tuple[int, int]] = None

    max_flight_duration_in_hours: Optional[int] = None

    flight_max_stops: Optional[int] = None

    destination: Optional[str] = None
    destination_type: Optional[DestinationType] = None

    limit: int = 250

    @staticmethod
    def from_subscription(subscription: Subscription):
        return GetDestinationsRequest(
            currency_code=subscription.currency,
            airport_code=subscription.depart_airport,
            max_budget=subscription.max_budget,

            depart_date=subscription.depart_date,
            return_date=subscription.return_date,
            exact_dates=subscription.exact_dates,

            trip_duration_range_in_days=subscription.trip_duration_range_in_days,
            max_flight_duration_in_hours=subscription.flight_max_duration_in_hours,
            flight_max_stops=subscription.flight_max_stops,

            destination=subscription.destination,
            destination_type=subscription.destination_type,
        )
