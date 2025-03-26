from dataclasses import dataclass

from app.domain.entities.airport import Airport


@dataclass
class FlightToTrack:
    depart: Airport
    destination: Airport
