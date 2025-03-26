from abc import abstractmethod, ABC
from typing import Optional, List

from app.domain.entities.subscriber import Subscriber


class ISubscriberRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Subscriber]:
        pass
    
    @abstractmethod
    def get_all(self) -> Optional[List[Subscriber]]:
        pass
