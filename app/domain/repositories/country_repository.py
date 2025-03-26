from abc import abstractmethod, ABC
from typing import Optional

from app.domain.entities.country import Country


class ICountryRepository(ABC):

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Country]:
        pass

