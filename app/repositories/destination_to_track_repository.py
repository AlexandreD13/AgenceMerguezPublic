from typing import List

import app.model_converter
from app import models
from app.domain.entities.destination_to_track import DestinationToTrack
from app.domain.repositories.destination_to_track_repository import IDestinationToTrackRepository


class DestinationToTrackRepository(IDestinationToTrackRepository):
    def get_all(self) -> List[DestinationToTrack]:
        rows = models.DestinationToTrack.objects.all()

        if not rows:
            return []
        else:
            return [app.model_converter.Mapper.destination_to_track_to_domain(row) for row in rows]
