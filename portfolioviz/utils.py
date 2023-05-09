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


## https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
def singleton(class_):
    class class_w(class_):
        _instance = None
        def __new__(class_, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w,
                                    class_).__new__(class_,
                                                    *args,
                                                    **kwargs)
                class_w._instance._sealed = False
            return class_w._instance
        def __init__(self, *args, **kwargs):
            if self._sealed:
                return
            super(class_w, self).__init__(*args, **kwargs)
            self._sealed = True
    class_w.__name__ = class_.__name__
    return class_w
