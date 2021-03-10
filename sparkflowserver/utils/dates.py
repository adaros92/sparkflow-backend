import datetime


def get_today() -> datetime.datetime:
    """Returns today as a datetime object"""
    return datetime.datetime.now()


def get_today_str(formatting: str = "%Y-%m-%d") -> str:
    """Returns today as a string"""
    return get_today().strftime(formatting)


def get_date_range(lookback_days: int, from_date: datetime.datetime = get_today()) -> list:
    """Returns a list of datetime objects in the range provided by reference date and lookback days from that
    date

    :param lookback_days the number of days to look back from the from_date to create the range
    :returns a list of dates in the range
    """
    return [from_date - datetime.timedelta(days=x) for x in range(lookback_days)]


def get_string_date_range(
        lookback_days: int, from_date: datetime.datetime = get_today(), formatting: str = "%Y-%m-%d") -> list:
    """Returns a list of string datetimes in the range provided by reference date and lookback days from that
    date

    :param lookback_days the number of days to look back from the from_date to create the range
    :returns a list of string dates in the range
    """
    date_range = get_date_range(lookback_days, from_date)
    return [datetime_object.strftime(formatting) for datetime_object in date_range]
