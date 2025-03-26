from abc import abstractmethod, ABC
from typing import List

from app.domain.entities.destination_to_track import DestinationToTrack


class IDestinationToTrackRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DestinationToTrack]:
        pass
