from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid___setitem___01():
    '''Items can be set as though the QGrid was flattened,
    and the "next" value is included.
    '''

    q = QGrid([0, [0, 0], 0], 0)

    q[0] = 1
    q[1] = 2
    q[2] = 3
    q[3] = 4
    q[4] = 5

    assert q == QGrid([1, [2, 3], 4], 5)


def test_quantizationtools_QGrid___setitem___02():
    '''Items in a QGrid may be set to a Number, None, a QEvent,
    an empty tuple, a tuple of Numbers or a tuple of QEvents.
    '''

    q = QGrid([0, [0, [0, 0]], 0], 0)

    q[0] = 0.5
    q[1] = None
    q[2] = QEvent(0, 0)
    q[3] = tuple([])
    q[4] = (0.5, 1, 3)
    q[5] = (QEvent(0, 0), QEvent(1, 1))

    assert q == QGrid([0.5, [None, [QEvent(0, 0), tuple([])]], (0.5, 1, 3)], (QEvent(0, 0), QEvent(1, 1)))
