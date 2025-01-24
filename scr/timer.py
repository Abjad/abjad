#! /usr/bin/env python

"""
Called by abjad.contextmanager.Timer on __enter__().
"""

import sys
import time

interval = int(sys.argv[1])
i = 0
while True:
    time.sleep(interval)
    i += interval
    unit = "seconds"
    if i == 1:
        unit = "second"
    message = "\n[{} {}]"
    message = message.format(i, unit)
    print(message)
