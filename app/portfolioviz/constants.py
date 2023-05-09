from portfolioviz.settings import DATE_FORMAT
from datetime import datetime

INITIAL_DATE = datetime.strptime("2022-02-14", DATE_FORMAT).date()

INITIAL_VALUE = 1_000_000_000