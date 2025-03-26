from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.deal_report import DealsReport
from app.domain.entities.destination import Destination


class IDealsReportRepository(ABC):

    @abstractmethod
    def create(self,destinations: List[Destination]) -> str:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> DealsReport:
        pass


    @abstractmethod
    def list(self) -> List[DealsReport]:
        pass
