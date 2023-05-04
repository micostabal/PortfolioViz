from typing import Iterable
from portfolioviz.settings import DATE_FORMAT
from datetime import date
from datetime import datetime

def parse_request_date(str_date: str) -> date:
    if str_date is None: return None
    return datetime.strptime(str_date, DATE_FORMAT).date()

def parse_query_param(request, key) -> str:
    return request.GET.get(key, None)

def to_dict_mapper(iterable: Iterable):
    return list(map(lambda x: x.to_dict(), iterable))