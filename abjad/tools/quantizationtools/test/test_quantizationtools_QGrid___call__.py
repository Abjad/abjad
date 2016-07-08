# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.quantizationtools import *


def test_quantizationtools_QGrid___call___01():

    q_grid = QGrid()
    a = QEventProxy(SilentQEvent(0,        ['A']), 0)
    b = QEventProxy(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = QEventProxy(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = QEventProxy(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = QEventProxy(SilentQEvent((11, 20), ['E']), (11, 20))
    f = QEventProxy(SilentQEvent((19, 20), ['F']), (19, 20))
    g = QEventProxy(SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert len(result) == 1
    assert format(result[0]) == "c'4"

    annotation = inspect_(result[0]).get_indicator(indicatortools.Annotation)

    assert isinstance(annotation.value, tuple) and len(annotation.value) == 4
    assert annotation.value[0].attachments == ('A',)
    assert annotation.value[1].attachments == ('B',)
    assert annotation.value[2].attachments == ('C',)
    assert annotation.value[3].attachments == ('D',)


def test_quantizationtools_QGrid___call___02():

    q_grid = QGrid()
    q_grid.subdivide_leaves([(0, (1, 1, 1))])
    q_grid.subdivide_leaves([(1, (1, 1))])
    q_grid.subdivide_leaves([(-2, (1, 1, 1))])
    a = QEventProxy(SilentQEvent(0,        ['A']), 0)
    b = QEventProxy(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = QEventProxy(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = QEventProxy(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = QEventProxy(SilentQEvent((11, 20), ['E']), (11, 20))
    f = QEventProxy(SilentQEvent((19, 20), ['F']), (19, 20))
    g = QEventProxy(SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert isinstance(result, list) and len(result) == 1
    assert format(result[0]) == stringtools.normalize(
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

    leaves = select(result[0]).by_leaf()
    leaf = leaves[0]
    annotation = inspect_(leaf).get_indicators(indicatortools.Annotation)[0]
    assert isinstance(annotation.value, tuple) and len(annotation.value) == 2
    assert annotation.value[0].attachments == ('A',)
    assert annotation.value[1].attachments == ('B',)

    leaf = leaves[1]
    assert not inspect_(leaf).get_indicators(indicatortools.Annotation)

    leaf = leaves[2]
    annotation = inspect_(leaf).get_indicator(indicatortools.Annotation)

    assert isinstance(annotation.value, tuple) and len(annotation.value) == 3
    assert annotation.value[0].attachments == ('C',)
    assert annotation.value[1].attachments == ('D',)
    assert annotation.value[2].attachments == ('E',)

    for leaf in leaves[3:6]:
        assert not inspect_(leaf).get_indicators(indicatortools.Annotation)


def test_quantizationtools_QGrid___call___03():
    r'''Non-binary works too.
    '''

    q_grid = QGrid()
    q_grid.subdivide_leaves([(0, (1, 1))])

    a = QEventProxy(SilentQEvent(0,        ['A']), 0)
    b = QEventProxy(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = QEventProxy(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = QEventProxy(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = QEventProxy(SilentQEvent((11, 20), ['E']), (11, 20))
    f = QEventProxy(SilentQEvent((19, 20), ['F']), (19, 20))
    g = QEventProxy(SilentQEvent(1,        ['G']), 1)

    q_grid.fit_q_events([a, b, c, d, e, f, g])

    result = q_grid((1, 3))

    assert isinstance(result, list) and len(result) == 1
    assert format(result[0]) == stringtools.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'4
            c'4
        }
        '''
        )
