from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from app.domain.entities.destination import DestinationPartial, Destination


@dataclass_json
@dataclass
class GetDestinationResponsePartial:
    destinations: List[DestinationPartial]


@dataclass_json
@dataclass
class GetDestinationResponse:
    destinations: List[Destination]
