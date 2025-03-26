import dataclasses
import json
from collections import defaultdict
from typing import List, Optional, Dict

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from loguru import logger

from app.domain.entities.destination import Destination
from app.domain.entities.monthly_historic_metric import MonthlyHistoricMetricForAirport
from app.domain.entities.subscriber import Subscriber
from app.domain.entities.subscription import SubscriptionWithDestinations
from app.domain.repositories.monthly_historic_metric_repository import IMonthlyHistoricMetricRepository
from app.domain.services.notifier_service import INotifierService
from app.utils.collections import flat_map


@dataclasses.dataclass
class DestinationDeal:
    destination: Destination
    discounted_percent: Optional[int]
    average: Optional[int]
    generic_deal: bool = False


class NotifierService(INotifierService):
    _monthly_metric: IMonthlyHistoricMetricRepository

    def __init__(self, monthly_historic_metric_repository: IMonthlyHistoricMetricRepository):
        self._monthly_metric = monthly_historic_metric_repository

    def notify(self, subscriptions_with_destinations: List[SubscriptionWithDestinations],
               generic_deals: List[Destination], subscriber: Subscriber):
        user_deals = self.__prepare_destination_deals(
            flat_map(lambda x: x.destinations, subscriptions_with_destinations),
            subscriber
        )

        other_deals = []

        if subscriber.subscribe_to_generic_deals:
            other_deals = self.__prepare_destination_deals(
                generic_deals,
                subscriber
            )
            # Mark the generic deals
            for d in other_deals:
                d.generic_deal = True

        deals = user_deals + other_deals

        if not deals:
            logger.warning(f"No new deals found for {subscriber.email}")
            return

        merge_data = {
            "subject": "New deals for you !",
            "header_content": f"Great Flight Deals for {len(deals)} destinations",
            "footer_content": "Sincerely, the Merguez Team",
            "destinations_with_subscription": deals,
        }

        text_content = ""
        for x in deals:
            text_content += f"{x.destination.city.name}: {x.destination.clickoutUrl}\n"

        html_content = render_to_string("email.html", merge_data)

        msg = EmailMultiAlternatives(f"Here are your deals for ...",
                                     text_content,
                                     "replaced@hotmail.com",
                                     [subscriber.email])
        msg.attach_alternative(html_content, "text/html")
        logger.info(f"Sending email to {subscriber.email}")
        msg.send()
        logger.info(f"Email successfully sent")

        # Now we update the cache to prevent new emails from being sent to this users
        self.__mark_destinations_as_sent(deals, subscriber)

    def __prepare_destination_deals(self, destinations: List[Destination], subscriber: Subscriber) -> List[
        DestinationDeal]:
        deals: List[DestinationDeal] = []

        for destination in destinations:
            if not self.__can_be_send(subscriber.email, destination):
                continue

            destination_metrics = self.__get_monthly_metric(destination)

            discounted_percent: Optional[int] = None
            average_price: Optional[int] = None

            if destination_metrics:
                discounted_percent = int((1 - destination.price / destination_metrics.average_price) * 100)

                if discounted_percent <= 0:
                    discounted_percent = None

                average_price = destination_metrics.average_price

            deals.append(
                DestinationDeal(
                    destination,
                    discounted_percent,
                    average_price
                )
            )

        return deals

    def __get_monthly_metric(self, destination: Destination) -> Optional[MonthlyHistoricMetricForAirport]:
        origin_airport = destination.originAirport
        destination_airport = destination.destinationAirport

        return self._monthly_metric.get_airport_historic_for_month(
            origin_airport,
            destination_airport,
            destination.depart_date.month
        )

    def __can_be_send(self, subscriber_email: str, destination: Destination) -> bool:
        key = self.hash_viewed_destination(subscriber_email, destination)
        result = cache.get(key)

        if result is None:
            return True

        cache_value = json.loads(result)

        if destination.price < cache_value['price']:
            return True

        return False

    def __mark_destinations_as_sent(
        self,
        deals: List[DestinationDeal],
        subscriber: Subscriber
    ):
        deals_by_hash_key: Dict[str, List[Destination]] = defaultdict(list)

        # Aggregate deals by hash key as we only want to set one of those values
        for d in deals:
            destination = d.destination
            key = self.hash_viewed_destination(subscriber.email, destination)
            deals_by_hash_key[key].append(destination)

        for key, group_deals in deals_by_hash_key.items():
            best_deal = min(group_deals, key=lambda d: d.price)
            cache_value = {
                'url': best_deal.clickoutUrl,
                'price': best_deal.price
            }
            cache.set(key, value=json.dumps(cache_value), timeout=60 * 60 * 24 * 7)

    @staticmethod
    def hash_viewed_destination(user: str, d: Destination) -> str:
        destination_hash = d.hash()
        return ':'.join(["viewed_destinations", user, destination_hash])
