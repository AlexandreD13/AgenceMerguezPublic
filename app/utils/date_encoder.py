import datetime

def date_to_str(d: datetime.date) -> str:
    return d.strftime("%Y%m%d")


def date_to_day_month_year(d: datetime.date) -> str:
    return d.strftime("%d/%m/%Y")


def str_to_date(d: str) -> datetime.date:
    return datetime.datetime.strptime(d, "%Y%m%d").date()

def str_to_datetime(d: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(d)

def datetime_to_str(d: datetime.datetime) -> str:
    return d.isoformat()
