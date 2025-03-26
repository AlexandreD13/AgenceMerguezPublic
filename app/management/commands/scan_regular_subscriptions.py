from django.core.management.base import BaseCommand
from loguru import logger


class Command(BaseCommand):
    def handle(self, **options):
        logger.info("Running scan_regular_subscriptions")
        from app.tasks import scan_all_subscribers

        scan_all_subscribers()

#
# if __name__ == "__main__":
#     import django
#
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agence.settings")
#     django.setup()
