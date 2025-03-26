import dataclasses
from datetime import datetime
from typing import Optional, List, Tuple

from app.domain.entities.destination import Destination
from app.domain.entities.destination_type import DestinationType
from app.domain.entities.subscriber import Subscriber


@dataclasses.dataclass
class Subscription:
    id: str

    subscribers: List[Subscriber]
    currency: str

    depart_airport: str
    max_budget: Optional[float]

    destination: str
    destination_type: DestinationType

    depart_date: Optional[datetime.date]
    return_date: Optional[datetime.date]

    # Whether it should match exactly the departure/return date.
    exact_dates: Optional[bool]

    trip_duration_range_in_days: Optional[Tuple[int, int]]

    flight_max_duration_in_hours: Optional[int]

    flight_max_stops: Optional[int]

    vip: Optional[bool]

    enabled: bool


@dataclasses.dataclass
class SubscriptionWithDestinations:
    subscription: Subscription
    destinations: List[Destination]
