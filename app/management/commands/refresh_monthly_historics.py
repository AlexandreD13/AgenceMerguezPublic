from django.core.management import BaseCommand
from loguru import logger


class Command(BaseCommand):
    def handle(self, **options):
        logger.info("Running refresh_monthly_historic")
        from app.tasks import refresh_monthly_historic

        refresh_monthly_historic()
