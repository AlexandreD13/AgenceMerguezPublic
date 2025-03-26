from datetime import datetime
from statistics import mean
from typing import Optional, List, Dict

from django.utils import timezone

from app import models
from app.domain.entities.airport import Airport
from app.domain.entities.country import Country
from app.domain.entities.monthly_historic_metric import MonthlyHistoricMetricForAirport, MonthlyHistoricMetricForCountry
from app.domain.repositories.monthly_historic_metric_repository import IMonthlyHistoricMetricRepository
from app.model_converter import Mapper


class MonthlyHistoricMetricRepository(IMonthlyHistoricMetricRepository):
    def get_country_historic(
        self,
        origin_airport: Airport,
        destination: Country
    ) -> List[MonthlyHistoricMetricForCountry]:
        rows = models.MonthlyHistoric.objects.filter(
            depart_airport=origin_airport.code
        ).filter(
            destination_country_code=destination.code
        ).all()

        if not rows:
            return []

        acc_by_month: Dict[int, MonthlyHistoricMetricForCountry] = {}

        for row in rows:
            month = row.month_identifier
            if month not in acc_by_month:
                acc_by_month[month] = MonthlyHistoricMetricForCountry(
                    origin=origin_airport,
                    destination=destination,
                    month_identifier=month,
                    minimum_price=row.minimum_price,
                    average_price=row.average_price,
                    maximum_price=row.maximum_price,
                    last_refresh_datetime=datetime.now(),
                    number_of_datapoints=1
                )
            else:
                acc = acc_by_month[month]
                acc.minimum_price = min(acc.minimum_price, row.minimum_price)
                acc.average_price = mean([acc.average_price, row.average_price])
                acc.maximum_price = max(acc.maximum_price, row.maximum_price)
                acc.number_of_datapoints += 1

        return list(acc_by_month.values())

    def get_country_historic_for_month(
        self,
        origin_airport: Airport,
        destination: Country,
        month: int
    ) -> Optional[MonthlyHistoricMetricForCountry]:
        rows = models.MonthlyHistoric.objects.filter(
            depart_airport=origin_airport.code
        ).filter(
            destination_country_code=destination.code
        ).filter(
            month_identifier=month
        ).all()

        if not rows:
            return None

        acc = MonthlyHistoricMetricForCountry(
            origin=origin_airport,
            destination=destination,
            month_identifier=month,
            minimum_price=rows[0].minimum_price,
            average_price=rows[0].average_price,
            maximum_price=rows[0].maximum_price,
            last_refresh_datetime=datetime.now(),
            number_of_datapoints=1
        )

        for n in rows[1:]:
            acc.minimum_price = min(acc.minimum_price, n.minimum_price)
            acc.average_price = mean([acc.average_price, n.average_price])
            acc.maximum_price = max(acc.maximum_price, n.maximum_price)
            acc.number_of_datapoints += 1

        return acc

    def get_airport_historic_for_month(
        self,
        origin_airport: Airport,
        destination_airport: Airport,
        month: int
    ) -> Optional[MonthlyHistoricMetricForAirport]:
        rows = models.MonthlyHistoric.objects.filter(
            depart_airport=origin_airport.code
        ).filter(
            destination_airport=destination_airport.code,
        ).filter(
            month_identifier=month
        ).first()

        if not rows:
            return None

        return Mapper.monthly_historic_to_domain(rows)

    def get_airport_historic(
        self,
        origin_airport: Airport,
        destination_airport: Airport
    ) -> List[MonthlyHistoricMetricForAirport]:
        rows = models.MonthlyHistoric.objects.filter(
            depart_airport=origin_airport.code
        ).filter(
            destination_airport=destination_airport.code,
        ).first()

        if not rows:
            return []

        return [Mapper.monthly_historic_to_domain(n) for n in rows]

    def upsert(self, monthly_metric: MonthlyHistoricMetricForAirport, origin_airport: Airport,
               destination_airport: Airport):
        updated = models.MonthlyHistoric.objects.filter(
            depart_airport=monthly_metric.depart_airport
        ).filter(
            destination_airport=monthly_metric.destination_airport
        ).filter(
            month_identifier=monthly_metric.month_identifier
        ).update(
            minimum_price=monthly_metric.minimum_price,
            average_price=monthly_metric.average_price,
            maximum_price=monthly_metric.maximum_price,
            number_of_datapoints=monthly_metric.number_of_datapoints,
            last_refresh_datetime=timezone.now()
        )

        if not updated:
            # We create instead
            models.MonthlyHistoric.objects.create(
                depart_airport=origin_airport.code,
                depart_country_code=origin_airport.country_code,

                destination_airport=destination_airport.code,
                destination_country_code=destination_airport.country_code,

                month_identifier=monthly_metric.month_identifier,

                minimum_price=monthly_metric.minimum_price,
                average_price=monthly_metric.average_price,
                maximum_price=monthly_metric.maximum_price,
                number_of_datapoints=monthly_metric.number_of_datapoints,
                last_refresh_datetime=timezone.now()
            )
