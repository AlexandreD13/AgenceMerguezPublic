from typing import Optional

import app.model_converter
from app import models
from app.domain.entities import subscription
from app.domain.entities.paging import PageResult
from app.domain.entities.subscriber import Subscriber
from app.domain.repositories.subscription_repository import ISubscriptionRepository


class SubscriptionRepository(ISubscriptionRepository):
    def list_for_subscriber(self, subscriber: Subscriber, vip_only: Optional[bool] = None) -> PageResult[
        subscription.Subscription]:
        query = models.Subscription.objects.filter(subscribers__id=subscriber.id).filter(enabled=True)

        if vip_only is not None:
            query = query.filter(vip=vip_only)

        results_domain = [app.model_converter.Mapper.subscription_to_domain(r, subscriber) for r in query]

        return PageResult(
            results=results_domain,
            total_count=len(results_domain)
        )
