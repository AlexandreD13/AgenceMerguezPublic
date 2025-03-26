from abc import abstractmethod, ABC
from typing import Optional


class IFeatureFlagRepository(ABC):

    @abstractmethod
    def is_active(self,flag: str, user_email: Optional[str] = None) -> bool:
        pass
