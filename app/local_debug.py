import os

if __name__ == "__main__":
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agence.settings")
    django.setup()


    # from app.repositories.deals_report_repository import DealsReportRepository
    # repo = DealsReportRepository()
    #
    # created_id = repo.create([
    # ])
    #
    # values = repo.list()

    from app.tasks import refresh_monthly_historic, scan_deals_user_only
    refresh_monthly_historic()

    #from app.tasks import scan_all_subscribers
    #scan_all_subscribers()

    from app.tasks import scan_deals
