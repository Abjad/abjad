# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_QGrid___eq___01():
    a = quantizationtools.QGrid()
    b = quantizationtools.QGrid()
    assert format(a) == format(b)
    assert a != b


def test_quantizationtools_QGrid___eq___02():
    a = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(
            preprolated_duration=1,
            children=[
                quantizationtools.QGridLeaf(
                    preprolated_duration=1,
                    q_event_proxies=[
                        quantizationtools.QEventProxy(
                            quantizationtools.SilentQEvent(100),
                            0.5,
                            ),
                        ],
                    ),
                ],
            ),
        next_downbeat=quantizationtools.QGridLeaf(
            preprolated_duration=1,
            q_event_proxies=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9,
                    ),
                ],
            ),
        )
    b = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(
            preprolated_duration=1,
            children=[
                quantizationtools.QGridLeaf(
                    preprolated_duration=1,
                    q_event_proxies=[
                        quantizationtools.QEventProxy(
                            quantizationtools.SilentQEvent(100),
                            0.5,
                            ),
                        ],
                    ),
                ],
            ),
        next_downbeat=quantizationtools.QGridLeaf(
            preprolated_duration=1,
            q_event_proxies=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9,
                    ),
                ],
            ),
        )
    assert format(a) == format(b)
    assert a != b


def test_quantizationtools_QGrid___eq___03():
    a = quantizationtools.QGrid()
    b = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(
            preprolated_duration=1,
            children=[
                quantizationtools.QGridLeaf(
                    preprolated_duration=1,
                    q_event_proxies=[
                        quantizationtools.QEventProxy(
                            quantizationtools.SilentQEvent(100),
                            0.5
                            )
                        ],
                    ),
                ],
            ),
        )
    c = quantizationtools.QGrid(
        next_downbeat=quantizationtools.QGridLeaf(
            preprolated_duration=1,
            q_event_proxies=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9
                    ),
                ],
            ),
        )
    d = quantizationtools.QGrid(
        root_node=quantizationtools.QGridContainer(
            preprolated_duration=1,
            children=[
                quantizationtools.QGridLeaf(
                    preprolated_duration=1,
                    q_event_proxies=[
                        quantizationtools.QEventProxy(
                            quantizationtools.SilentQEvent(100),
                            0.5
                            ),
                        ],
                    ),
                ],
            ),
        next_downbeat=quantizationtools.QGridLeaf(
            preprolated_duration=1,
            q_event_proxies=[
                quantizationtools.QEventProxy(
                    quantizationtools.TerminalQEvent(200),
                    0.9,
                    ),
                ],
            ),
        ),

    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
