from typing import Optional, List

import app.model_converter
from app import models
from app.domain.entities.subscriber import Subscriber
from app.domain.repositories.subscriber_repository import ISubscriberRepository


class SubscriberRepository(ISubscriberRepository):

    def get_by_email(self, email: str) -> Optional[Subscriber]:
        row = models.Subscriber.objects.filter(email=email).first()

        if not row:
            return None
        else:
            return app.model_converter.Mapper.subscriber_to_domain(row)

    def get_all(self) -> Optional[List[Subscriber]]:
        rows = models.Subscriber.objects.all()

        if not rows:
            return None
        else:
            return [app.model_converter.Mapper.subscriber_to_domain(row) for row in rows]
