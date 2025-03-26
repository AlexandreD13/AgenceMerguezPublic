from app.domain.entities import subscription, destination_type, subscriber, destination_to_track, \
    monthly_historic_metric, deal_report
from app.models import Subscription, Subscriber, DestinationType, DestinationToTrack, MonthlyHistoric, DealsReporting


class Mapper:

    @staticmethod
    def subscription_to_domain(s: Subscription, subscriber: Subscriber) -> subscription.Subscription:
        trip_duration_range_in_days = None

        if s.trip_duration_in_days_min or s.trip_duration_in_days_max:
            trip_duration_range_in_days = (s.trip_duration_in_days_min or 1, s.trip_duration_in_days_max or 999)

        destination_code = ""
        d_type = ""

        if s.destination_airport:
            destination_code = s.destination_airport.airport_code
            d_type = destination_type.DestinationType.AIRPORT
        elif s.destination_country:
            destination_code = s.destination_country.country_code
            d_type = destination_type.DestinationType.COUNTRY

        return subscription.Subscription(
            id=s.pk,
            depart_airport=s.depart_airport,
            max_budget=s.max_budget,
            subscribers=[Mapper.subscriber_to_domain(sub) for sub in s.subscribers.all()],
            currency=s.currency or subscriber.currency,
            depart_date=s.depart_date,
            return_date=s.return_date,
            trip_duration_range_in_days=trip_duration_range_in_days,
            flight_max_duration_in_hours=s.flight_max_duration_in_hours,
            flight_max_stops=s.flight_max_stops,
            exact_dates=s.exact_dates,
            vip=s.vip,
            enabled=s.enabled,
            destination=destination_code,
            destination_type=d_type
        )

    @staticmethod
    def destination_type_to_domain(c: DestinationType) -> destination_type.DestinationType:
        if c == DestinationType.AIRPORT:
            return destination_type.DestinationType.AIRPORT

        return destination_type.DestinationType.COUNTRY

    @staticmethod
    def subscriber_to_domain(s: Subscriber) -> subscriber.Subscriber:
        return subscriber.Subscriber(
            id=s.pk,
            first_name=s.first_name,
            last_name=s.last_name,
            email=s.email,
            preferred_airport=s.preferred_airport,
            currency=s.currency,
            subscribe_to_generic_deals=s.subscribe_to_generic_deals
        )

    @staticmethod
    def destination_to_track_to_domain(c: DestinationToTrack) -> destination_to_track.DestinationToTrack:
        if c.destination_country:
            return destination_to_track.DestinationToTrack(
                c.origin_airport.airport_code,
                # todo: it could be converted to domain object
                c.destination_country.country_code,
                destination_type.DestinationType.COUNTRY
            )
        elif c.destination_airport:
            return destination_to_track.DestinationToTrack(
                c.origin_airport.airport_code,
                # todo: it could be converted to domain object
                c.destination_airport.airport_code,
                destination_type.DestinationType.AIRPORT
            )
        else:
            raise ValueError("unknown  object")

    @staticmethod
    def monthly_historic_to_domain(mh: MonthlyHistoric) -> monthly_historic_metric.MonthlyHistoricMetricForAirport:
        return monthly_historic_metric.MonthlyHistoricMetricForAirport(
            depart_airport=mh.depart_airport,
            destination_airport=mh.destination_airport,
            month_identifier=mh.month_identifier,
            minimum_price=mh.minimum_price,
            average_price=mh.average_price,
            maximum_price=mh.maximum_price,
            last_refresh_datetime=mh.last_refresh_datetime,
            number_of_datapoints=mh.number_of_datapoints
        )

    @staticmethod
    def deals_report_to_domain(d: DealsReporting) -> deal_report.DealsReport:
        return deal_report.DealsReport(
            id=d.pk,
            deals=d.deals_json,
            created_at=d.created_at
        )
