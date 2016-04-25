# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_QGridLeaf___eq___01():
    a = quantizationtools.QGridLeaf(1, [])
    b = quantizationtools.QGridLeaf(1, [])
    assert format(a) == format(b)
    assert a != b


def test_quantizationtools_QGridLeaf___eq___02():
    a = quantizationtools.QGridLeaf(1, [])
    b = quantizationtools.QGridLeaf(1, [quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1000), 0.5)])
    c = quantizationtools.QGridLeaf(2, [])
    d = quantizationtools.QGridLeaf(2, [quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1000), 0.5)])
    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
