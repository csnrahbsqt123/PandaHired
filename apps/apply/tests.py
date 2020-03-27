import datetime
import time
import math
from django.test import TestCase

# Create your tests here.
ftime="2018-08-01"


def work_time(ftime):
    date1 = datetime.datetime.strftime(ftime, "%Y-%m-%d")
    a = date1.timestamp()
    b = time.time()
    c = (b - a) / 60 / 60 / 24

    if c < 365:
        print(c / 30)
        c = str(math.ceil(c / 30)) + "月"
        return c
    else:
        c = str(math.ceil(c / 365)) + "年"
        return c
