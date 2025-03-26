from django.core.management import BaseCommand
from loguru import logger


class Command(BaseCommand):
    def handle(self, **options):
        logger.info("Running scan_all_vip_subscriptions")
        from app.tasks import scan_all_vip_subscriptions

        scan_all_vip_subscriptions()
