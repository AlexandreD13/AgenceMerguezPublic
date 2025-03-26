from abc import abstractmethod, ABC
from typing import Optional

from app.domain.entities.airport import Airport


class IAirportRepository(ABC):

    @abstractmethod
    def get_by_code(self, code: str) -> Airport:
        pass

