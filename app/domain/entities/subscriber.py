import dataclasses
from typing import Optional


@dataclasses.dataclass
class Subscriber:
    id: str
    first_name: str
    last_name: str
    email: str

    preferred_airport: Optional[str]
    currency: str
    subscribe_to_generic_deals: bool
