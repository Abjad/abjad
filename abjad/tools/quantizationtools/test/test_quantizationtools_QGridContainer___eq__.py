# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_QGridContainer___eq___01():

    a = quantizationtools.QGridContainer(preprolated_duration=1, children=[])
    b = quantizationtools.QGridContainer(preprolated_duration=1, children=[])

    assert format(a) == format(b)
    assert a != b


def test_quantizationtools_QGridContainer___eq___02():

    a = quantizationtools.QGridContainer(preprolated_duration=1, children=[
        quantizationtools.QGridLeaf(preprolated_duration=1)
        ])
    b = quantizationtools.QGridContainer(preprolated_duration=1, children=[
        quantizationtools.QGridLeaf(preprolated_duration=1)
        ])

    assert format(a) == format(b)
    assert a != b


def test_quantizationtools_QGridContainer___eq___03():

    a = quantizationtools.QGridContainer(preprolated_duration=1, children=[])
    b = quantizationtools.QGridContainer(preprolated_duration=2, children=[])
    c = quantizationtools.QGridContainer(preprolated_duration=1, children=[
        quantizationtools.QGridLeaf(preprolated_duration=1)
        ])
    d = quantizationtools.QGridContainer(preprolated_duration=2, children=[
        quantizationtools.QGridLeaf(preprolated_duration=1)
        ])
    e = quantizationtools.QGridContainer(preprolated_duration=2, children=[
        quantizationtools.QGridLeaf(2)
        ])

    assert a != b
    assert a != c
    assert a != d
    assert a != e
    assert b != c
    assert b != d
    assert b != e
    assert c != d
    assert c != e
    assert d != e
