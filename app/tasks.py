# Create your tasks here
from time import sleep
from typing import List

from dependency_injector.wiring import Provide, inject
from loguru import logger

from agence.celery import app
from agence.container import Container
from app.domain.repositories.airport_repository import IAirportRepository
from app.domain.repositories.destination_to_track_repository import IDestinationToTrackRepository
from app.domain.services.deal_scanner_service import IDealScannerService
from app.domain.services.historic_service import IHistoricService
from app.domain.services.notifier_service import INotifierService
from app.repositories.subscriber_repository import ISubscriberRepository


@app.task()
@inject
def scan_deals(subscriber_email: str, scanner: IDealScannerService = Provide[Container.deal_scanner_service],
               subscribers: ISubscriberRepository = Provide[Container.subscriber_repository],
               notifier: INotifierService = Provide[Container.notifier_service]):
    logger.info(f"Started global deal scan")
    # deals = scanner.scan_global_deals()
    #
    # if not deals:
    #     logger.warning("No deals found below the required threshold")
    deals = []

    logger.info(f"Starting per-subscriber scan")
    custom_deals = scanner.scan(subscriber_email, vip_only=None)
    subscriber = subscribers.get_by_email(subscriber_email)
    notifier.notify(custom_deals, deals, subscriber)


@app.task()
@inject
def scan_deals_user_only(
    subscriber_email: str,
    scanner: IDealScannerService = Provide[Container.deal_scanner_service],
    subscribers: ISubscriberRepository = Provide[Container.subscriber_repository],
    notifier: INotifierService = Provide[Container.notifier_service]
):
    # global_deal_response = scanner.scan_global_deals()

    # if not global_deal_response.destinations:
    #     logger.warning("No deals found below the required threshold")

    logger.info(f"Starting per-subscriber scan")
    custom_deals = scanner.scan(subscriber_email, vip_only=None)
    subscriber = subscribers.get_by_email(subscriber_email)
    notifier.notify(custom_deals, [], subscriber)


@app.task()
@inject
def scan_all_subscribers(scanner: IDealScannerService = Provide[Container.deal_scanner_service],
                         subscribers: ISubscriberRepository = Provide[Container.subscriber_repository],
                         notifier: INotifierService = Provide[Container.notifier_service]):
    logger.info(f"Started generic deal scan")
    # deals = scanner.scan_global_deals()
    #
    # if not deals:
    #     logger.warning("No deals found below the required threshold")
    deals = []
    subscribers_in_error: List[str] = []

    def mark_error(s: str):
        subscribers_in_error.append(s)

    logger.info(f"Starting per-subscriber scan")
    for subscriber in subscribers.get_all():
        with logger.catch(onerror=lambda _: mark_error(subscriber)):
            logger.info(f"Scanning for {subscriber.email}")
            custom_deals = scanner.scan(subscriber.email, vip_only=None)

            notifier.notify(custom_deals, deals, subscriber)

        # Pause a few seconds before sending another mail to avoid being throttled
        sleep(5)

    if subscribers_in_error:
        exit(1)


@app.task()
@inject
def scan_all_vip_subscriptions(
    scanner: IDealScannerService = Provide[Container.deal_scanner_service],
    subscribers: ISubscriberRepository = Provide[Container.subscriber_repository],
    notifier: INotifierService = Provide[Container.notifier_service]
):
    # deals = scanner.scan_global_deals()
    #
    # if not deals:
    #     logger.warning("No deals found below the required threshold")
    deals = []
    subscribers_in_error: List[str] = []

    def mark_error(s: str):
        subscribers_in_error.append(s)

    logger.info(f"Starting per-subscriber scan")
    for subscriber in subscribers.get_all():
        with logger.catch(onerror=lambda _: mark_error(subscriber)):
            logger.info(f"Scanning for {subscriber.email}")
            custom_deals = scanner.scan(subscriber.email, vip_only=True)

            notifier.notify(custom_deals, deals, subscriber)

        # Pause a few seconds before sending another mail to avoid being throttled
        sleep(5)

    if subscribers_in_error:
        exit(1)


@app.task()
@inject
def refresh_monthly_historic(
    destination_to_track_repository: IDestinationToTrackRepository = Provide[Container.destination_to_track_repository],
    historic_service: IHistoricService = Provide[Container.historic_service],
    airport_repository: IAirportRepository = Provide[Container.airport_repository]
):
    destinations_to_track = destination_to_track_repository.get_all()
    destination_in_error: List[str] = []

    def mark_error(s: str):
        destination_in_error.append(s)

    for destination in destinations_to_track:
        with logger.catch(onerror=lambda _: mark_error(str(destination))):
            airport = airport_repository.get_by_code(destination.origin_airport_code)
            logger.info(f"Start Refreshing for {destination}")
            historic_service.refresh_monthly_metrics(
                airport,
                destination.destination_code,
                destination.destination_type
            )
            logger.info(f"Done Refreshing")

    if destination_in_error:
        exit(1)
