# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_TerminalQEvent___eq___01():

    a = quantizationtools.TerminalQEvent(1000)
    b = quantizationtools.TerminalQEvent(1000)

    assert a == b


def test_quantizationtools_TerminalQEvent___eq___02():

    a = quantizationtools.TerminalQEvent(1000)
    b = quantizationtools.TerminalQEvent(9000)

    assert a != b


def test_quantizationtools_TerminalQEvent___eq___03():

    a = quantizationtools.TerminalQEvent(100)
    b = quantizationtools.PitchedQEvent(100, [0])
    c = quantizationtools.SilentQEvent(100)

    assert a != b
    assert a != c
