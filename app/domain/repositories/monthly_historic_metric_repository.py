from abc import abstractmethod, ABC
from typing import Optional, List

from app.domain.entities.airport import Airport
from app.domain.entities.country import Country
from app.domain.entities.monthly_historic_metric import MonthlyHistoricMetricForAirport, MonthlyHistoricMetricForCountry


class IMonthlyHistoricMetricRepository(ABC):

    @abstractmethod
    def get_country_historic(self, origin_airport: Airport, destination: Country) -> List[
        MonthlyHistoricMetricForCountry]:
        pass

    @abstractmethod
    def get_country_historic_for_month(self, origin_airport: Airport, destination: Country, month: int) -> Optional[
        MonthlyHistoricMetricForCountry]:
        pass

    @abstractmethod
    def get_airport_historic_for_month(self, origin_airport: Airport, destination_airport: Airport,
                                       month: int) -> Optional[
        MonthlyHistoricMetricForAirport]:
        pass

    @abstractmethod
    def get_airport_historic(self, origin_airport: Airport, destination_airport: Airport) -> List[
        MonthlyHistoricMetricForAirport]:
        pass

    @abstractmethod
    def upsert(self, monthly_metric: MonthlyHistoricMetricForAirport, origin_airport: Airport,
               destination_airport: Airport):
        pass
