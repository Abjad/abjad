from abjad.tools.timeintervaltools import *
import py.test


def test_TimeIntervalTree_duration_01():
    a = TimeInterval(-1, 2)
    b = TimeInterval(0, 1)
    c = TimeInterval(1, 3)

    tree = TimeIntervalTree(a)
    assert tree.duration == 3

    tree = TimeIntervalTree(b)
    assert tree.duration == 1

    tree = TimeIntervalTree(c)
    assert tree.duration == 2

    tree = TimeIntervalTree([a, b])
    assert tree.duration == 3

    tree = TimeIntervalTree([a, c])
    assert tree.duration == 4

    tree = TimeIntervalTree([b, c])
    assert tree.duration == 3

    tree = TimeIntervalTree([a, b, c])
    assert tree.duration == 4
