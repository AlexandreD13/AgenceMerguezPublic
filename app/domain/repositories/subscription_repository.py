from abc import abstractmethod, ABC
from typing import Optional

from app.domain.entities.paging import PageResult
from app.domain.entities.subscriber import Subscriber
from app.domain.entities.subscription import Subscription


class ISubscriptionRepository(ABC):

    @abstractmethod
    def list_for_subscriber(self, subscriber: Subscriber, vip_only: Optional[bool] = None) -> PageResult[Subscription]:
        pass
