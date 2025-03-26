from abc import abstractmethod, ABC

from app.domain.entities.airport import Airport
from app.domain.entities.destination_type import DestinationType


class IHistoricService(ABC):
    @abstractmethod
    def refresh_monthly_metrics(self, origin: Airport, destination_code: str, destination_type: DestinationType):
        pass
