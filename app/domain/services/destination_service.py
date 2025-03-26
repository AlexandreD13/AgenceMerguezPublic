
from abc import abstractmethod, ABC

from app.domain.repositories.dto.get_destination_request import GetDestinationsRequest
from app.domain.repositories.dto.get_destination_response import GetDestinationResponse


class IDestinationService(ABC):

    @abstractmethod
    def fetch(self, request: GetDestinationsRequest) -> GetDestinationResponse:
        pass
