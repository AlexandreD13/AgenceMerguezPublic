from dependency_injector import containers, providers

from agence.settings import KIWI_SEARCH_API_KEY
from app.repositories.airport_repository import AirportRepository
from app.repositories.country_repository import CountryRepository
from app.repositories.deals_report_repository import DealsReportRepository
from app.repositories.destination_to_track_repository import DestinationToTrackRepository
from app.repositories.destinations.kiwi.kiwi_destination_repository import KiwiDestinationRepository
from app.repositories.monthly_historic_metric_repository import MonthlyHistoricMetricRepository
from app.repositories.subscriber_repository import SubscriberRepository
from app.repositories.subscriptions_repository import SubscriptionRepository
from app.services.deal_scanner_service import DealScannerService
from app.services.destination_service import DestinationService
from app.services.historic_service import HistoricService
from app.services.notifier_service import NotifierService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Repositories
    airport_repository = providers.Singleton(
        AirportRepository
    )

    country_repository = providers.Singleton(
        CountryRepository
    )

    kiwi_destination_repository = providers.Singleton(
        KiwiDestinationRepository,
        KIWI_SEARCH_API_KEY
    )

    subscriptions_repository = providers.Singleton(
        SubscriptionRepository
    )

    subscriber_repository = providers.Singleton(
        SubscriberRepository
    )

    destination_to_track_repository = providers.Singleton(
        DestinationToTrackRepository
    )

    monthly_historic_metric_repository = providers.Singleton(
        MonthlyHistoricMetricRepository
    )

    deals_report_repository = providers.Singleton(
        DealsReportRepository
    )

    # Services
    notifier_service = providers.Singleton(
        NotifierService,
        monthly_historic_metric_repository,
    )

    destination_service = providers.Singleton(
        DestinationService,
        kiwi_destination_repository,
        country_repository,
        airport_repository
    )

    historic_service = providers.Singleton(
        HistoricService,
        destination_service,
        destination_to_track_repository,
        monthly_historic_metric_repository,
        airport_repository,
        country_repository
    )

    deal_scanner_service = providers.Singleton(
        DealScannerService,
        destination_service,
        notifier_service,
        subscriptions_repository,
        subscriber_repository,
        destination_to_track_repository,
        monthly_historic_metric_repository,
        deals_report_repository,
        airport_repository,
        country_repository
    )
