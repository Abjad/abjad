#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time


i = 0
while True:
    time.sleep(1)
    i += 1
    unit = 'seconds'
    if i == 1:
        unit = 'second'
    message = '{} {} ...'
    message = message.format(i, unit)
    print(message)