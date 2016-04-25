# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_QEventProxy___init___01():
    q_event = quantizationtools.PitchedQEvent(130, [0])
    proxy = quantizationtools.QEventProxy(q_event, 0.5)
    assert proxy.q_event == q_event
    assert proxy.offset == durationtools.Offset(1, 2)


def test_quantizationtools_QEventProxy___init___02():
    q_event = quantizationtools.PitchedQEvent(130, [0, 1, 4])
    proxy = quantizationtools.QEventProxy(q_event, 100, 1000)
    assert proxy.q_event == q_event
    assert proxy.offset == durationtools.Offset(1, 30)
