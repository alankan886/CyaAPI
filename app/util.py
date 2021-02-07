from datetime import datetime


def convert_str_to_date(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()
