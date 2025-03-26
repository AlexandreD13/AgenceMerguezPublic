from abc import abstractmethod, ABC

from app.domain.repositories.dto.get_destination_request import GetDestinationsRequest
from app.domain.repositories.dto.get_destination_response import GetDestinationResponsePartial


class IDestinationRepository(ABC):

    @abstractmethod
    def fetch(self, request: GetDestinationsRequest) -> GetDestinationResponsePartial:
        pass
