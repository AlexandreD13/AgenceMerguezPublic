from typing import List, Optional

import app.model_converter
from app import models
from app.domain.entities.deal_report import DealsReport
from app.domain.entities.destination import Destination
from app.domain.repositories.deals_report_repository import IDealsReportRepository


class DealsReportRepository(IDealsReportRepository):
    def create(self, destinations: List[Destination]) -> str:

        json = {'destinations': []}

        for destination in destinations:
            country = destination.destinationCountry
            value = {
                'origin': destination.originAirport.code,
                'destination': destination.destinationAirport.code,
                'continent': country.continent,
                'country': country.name,
                'depart_date': str(destination.depart_date),
                'return_date': str(destination.return_date),
                'price': destination.price,
                'url': destination.clickoutUrl,
            }
            json['destinations'].append(value)

        created = models.DealsReporting.objects.create(
            deals_json=json
        )

        return str(created.pk)

    def get_by_id(self, id: str) -> Optional[DealsReport]:
        row = models.DealsReporting.objects.get(pk=id)

        if not row:
            return None
        else:
            return app.model_converter.Mapper.deals_report_to_domain(row)

    def list(self) -> Optional[List[DealsReport]]:
        rows = models.DealsReporting.objects.all()

        if not rows:
            return None
        else:
            return [app.model_converter.Mapper.deals_report_to_domain(row) for row in rows]
