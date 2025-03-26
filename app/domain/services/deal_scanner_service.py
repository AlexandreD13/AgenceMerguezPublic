from abc import abstractmethod, ABC
from typing import Optional, List

from app.domain.entities.destination import Destination
from app.domain.entities.global_deals import GlobalDealsResponse
from app.domain.entities.subscription import SubscriptionWithDestinations


class IDealScannerService(ABC):

    @abstractmethod
    def scan(self, subscriber_email: str, vip_only: Optional[bool]) -> List[SubscriptionWithDestinations]:
        pass

    @abstractmethod
    def scan_global_deals(self) -> GlobalDealsResponse:
        pass
