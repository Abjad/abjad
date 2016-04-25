# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_PitchedQEvent___eq___01():

    a = quantizationtools.PitchedQEvent(1000, [0])
    b = quantizationtools.PitchedQEvent(1000, [0])

    assert a == b


def test_quantizationtools_PitchedQEvent___eq___02():

    a = quantizationtools.PitchedQEvent(1000, [0])
    b = quantizationtools.PitchedQEvent(1000, [0], ['foo', 'bar', 'baz'])
    c = quantizationtools.PitchedQEvent(9999, [0])
    d = quantizationtools.PitchedQEvent(1000, [0, 1, 4])

    assert a != b
    assert a != c
    assert a != d


def test_quantizationtools_PitchedQEvent___eq___03():

    a = quantizationtools.TerminalQEvent(100)
    b = quantizationtools.PitchedQEvent(100, [0])
    c = quantizationtools.SilentQEvent(100)

    assert a != b
    assert a != c
