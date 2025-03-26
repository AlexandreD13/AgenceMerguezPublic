from dataclasses import dataclass
from typing import List

from app.domain.entities.destination import Destination


@dataclass
class GlobalDealsResponse:
    destinations: List[Destination]
    report_page_id: str
