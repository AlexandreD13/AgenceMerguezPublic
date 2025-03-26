from dataclasses import dataclass
from datetime import datetime


@dataclass
class DealsReport:
    id: str
    # Later we could type this interface
    deals: dict
    created_at: datetime.date
