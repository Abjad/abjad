import datetime
import time


def get_current_date():
    return datetime.date(*time.localtime()[:3])
