from dataclasses import dataclass


@dataclass
class Country:
    code: str
    name: str
    continent: str
    continent_code: str
