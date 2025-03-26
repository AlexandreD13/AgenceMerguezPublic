from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.destination import Destination
from app.domain.entities.subscriber import Subscriber
from app.domain.entities.subscription import SubscriptionWithDestinations


class INotifierService(ABC):
    @abstractmethod
    def notify(self,
               subscriptions_with_destinations: List[SubscriptionWithDestinations],
               generic_deals: List[Destination],
               subscriber: Subscriber
               ):
        pass
