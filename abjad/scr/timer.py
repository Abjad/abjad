#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time


interval = int(sys.argv[1])
i = 0
while True:
    time.sleep(interval)
    i += interval
    unit = 'seconds'
    if i == 1:
        unit = 'second'
    message = '\n[{} {}]'
    message = message.format(i, unit)
    print(message)
