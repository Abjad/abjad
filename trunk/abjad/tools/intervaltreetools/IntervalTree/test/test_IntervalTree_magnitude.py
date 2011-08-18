from abjad.tools.intervaltreetools import *
import py.test


def test_IntervalTree_magnitude_01():
    a = BoundedInterval(-1, 2)
    b = BoundedInterval(0, 1)
    c = BoundedInterval(1, 3)

    tree = IntervalTree(a)
    assert tree.magnitude == 3

    tree = IntervalTree(b)
    assert tree.magnitude == 1

    tree = IntervalTree(c)
    assert tree.magnitude == 2

    tree = IntervalTree([a, b])
    assert tree.magnitude == 3

    tree = IntervalTree([a, c])
    assert tree.magnitude == 4

    tree = IntervalTree([b, c])
    assert tree.magnitude == 3

    tree = IntervalTree([a, b, c])
    assert tree.magnitude == 4
