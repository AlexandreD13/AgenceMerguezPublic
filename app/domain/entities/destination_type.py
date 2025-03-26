from enum import Enum, unique


@unique
class DestinationType(Enum):
    AIRPORT = "airport"
    COUNTRY = "country"

