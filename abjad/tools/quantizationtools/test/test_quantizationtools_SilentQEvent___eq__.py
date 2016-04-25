# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_SilentQEvent___eq___01():

    a = quantizationtools.SilentQEvent(1000)
    b = quantizationtools.SilentQEvent(1000)

    assert a == b


def test_quantizationtools_SilentQEvent___eq___02():

    a = quantizationtools.SilentQEvent(1000)
    b = quantizationtools.SilentQEvent(1000, ['foo', 'bar', 'baz'])
    c = quantizationtools.SilentQEvent(9999)

    assert a != b
    assert a != c
