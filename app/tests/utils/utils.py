import random
import string
from datetime import datetime


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def format_datetime(datetime: datetime) -> str:
    return datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
