from dataclasses import dataclass


@dataclass
class Airport:
    code: str
    country_code: str
    region_name: str

    latitude: float
    longitude: float

    name: str
    icao: str
