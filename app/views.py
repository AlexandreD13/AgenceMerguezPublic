from datetime import datetime

from dependency_injector.wiring import Provide, inject
from django.http import HttpResponse, Http404
from django.template import loader

from agence.container import Container
from app.domain.repositories.deals_report_repository import IDealsReportRepository


# Create your views here.
# https://docs.djangoproject.com/en/5.0/intro/tutorial03/#writing-more-views

@inject
def view(request, slug, deal_reports: IDealsReportRepository = Provide[Container.deals_report_repository]):
    deal_report = deal_reports.get_by_id(slug)

    if not deal_report:
        raise Http404("Report not found")

    template = loader.get_template("view_report.html")

    destinations = deal_report.deals['destinations']

    # Calculate the length in days for each flight
    for deal in destinations:
        depart_d = datetime.strptime(deal['depart_date'], "%Y-%m-%d")
        return_d = datetime.strptime(deal['return_date'], "%Y-%m-%d")

        deal['days'] = (return_d - depart_d).days

    context = {
        'id': deal_report.id,
        'date': deal_report.created_at,
        'deals': deal_report.deals['destinations']
    }
    return HttpResponse(template.render(context, request))
