from datetime import datetime


def format_datetime(input_dt: datetime) -> str:
    return input_dt.strftime("%H:%M %d.%m.%y")
