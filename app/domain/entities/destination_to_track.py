from dataclasses import dataclass

from app.domain.entities.destination_type import DestinationType


@dataclass
class DestinationToTrack:
    origin_airport_code: str
    destination_code: str
    destination_type: DestinationType
