# -*- coding: utf-8 -*-
import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_QGrid___call___01():

    q_grid = quantizationtools.QGrid()
    a = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(0,        ['A']), 0)
    b = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 20),  ['B']), (1, 20))
    c = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((9, 20),  ['C']), (9, 20))
    d = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 2),   ['D']), (1, 2))
    e = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((11, 20), ['E']), (11, 20))
    f = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((19, 20), ['F']), (19, 20))
    g = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert len(result) == 1
    assert format(result[0]) == "c'4"

    annotation = abjad.inspect(result[0]).get_indicator(dict)
    q_events = annotation['q_events']

    assert isinstance(q_events, tuple) and len(q_events) == 4
    assert q_events[0].attachments == ('A',)
    assert q_events[1].attachments == ('B',)
    assert q_events[2].attachments == ('C',)
    assert q_events[3].attachments == ('D',)


def test_quantizationtools_QGrid___call___02():

    q_grid = quantizationtools.QGrid()
    q_grid.subdivide_leaves([(0, (1, 1, 1))])
    q_grid.subdivide_leaves([(1, (1, 1))])
    q_grid.subdivide_leaves([(-2, (1, 1, 1))])
    a = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(0,        ['A']), 0)
    b = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 20),  ['B']), (1, 20))
    c = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((9, 20),  ['C']), (9, 20))
    d = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((1, 2),   ['D']), (1, 2))
    e = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((11, 20), ['E']), (11, 20))
    f = quantizationtools.QEventProxy(quantizationtools.SilentQEvent((19, 20), ['F']), (19, 20))
    g = quantizationtools.QEventProxy(quantizationtools.SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert isinstance(result, list) and len(result) == 1
    assert format(result[0]) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'8
            c'16
            c'16
            \times 2/3 {
                c'16
                c'16
                c'16
            }
        }
        '''
        )

    leaves = abjad.select(result[0]).by_leaf()
    leaf = leaves[0]
    annotation = abjad.inspect(leaf).get_indicator(dict)
    q_events = annotation['q_events']
    assert isinstance(q_events, tuple) and len(q_events) == 2
    assert q_events[0].attachments == ('A',)
    assert q_events[1].attachments == ('B',)

    leaf = leaves[1]
    assert not abjad.inspect(leaf).get_indicator(dict)

    leaf = leaves[2]
    annotation = abjad.inspect(leaf).get_indicator(dict)
    q_events = annotation['q_events']

    assert isinstance(q_events, tuple) and len(q_events) == 3
    assert q_events[0].attachments == ('C',)
    assert q_events[1].attachments == ('D',)
    assert q_events[2].attachments == ('E',)

    for leaf in leaves[3:6]:
        assert not abjad.inspect(leaf).get_indicators(dict)


def test_quantizationtools_QGrid___call___03():
    r'''Non-binary works too.
    '''

    q_grid = quantizationtools.QGrid()
    q_grid.subdivide_leaves([(0, (1, 1))])

    a = quantizationtools.QEventProxy(
        quantizationtools.SilentQEvent(0,        ['A']), 0)
    b = quantizationtools.QEventProxy(
        quantizationtools.SilentQEvent((1, 20),  ['B']), (1, 20))
    c = quantizationtools.QEventProxy(
        quantizationtools.SilentQEvent((9, 20),  ['C']), (9, 20))
    d = quantizationtools.QEventProxy(
        quantizationtools.SilentQEvent((1, 2),   ['D']), (1, 2))
    e = quantizationtools.QEventProxy(
        quantizationtools.SilentQEvent((11, 20), ['E']), (11, 20))
    f = quantizationtools.QEventProxy(
        quantizationtools.SilentQEvent((19, 20), ['F']), (19, 20))
    g = quantizationtools.QEventProxy(
        quantizationtools.SilentQEvent(1,        ['G']), 1)

    q_grid.fit_q_events([a, b, c, d, e, f, g])

    result = q_grid((1, 3))

    assert isinstance(result, list) and len(result) == 1
    assert format(result[0]) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'4
            c'4
        }
        '''
        )
