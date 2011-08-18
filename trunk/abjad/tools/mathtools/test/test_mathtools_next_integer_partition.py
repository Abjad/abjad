from abjad import *
from abjad.tools import mathtools


def test_mathtools_next_integer_partition_01():

    assert mathtools.next_integer_partition((8, )) == (7, 1)
    assert mathtools.next_integer_partition((7, 1)) == (6, 2)
    assert mathtools.next_integer_partition((6, 2)) == (6, 1, 1)
    assert mathtools.next_integer_partition((6, 1, 1)) == (5, 3)
    assert mathtools.next_integer_partition((5, 3)) == (5, 2, 1)
    assert mathtools.next_integer_partition((5, 2, 1)) == (5, 1, 1, 1)
    assert mathtools.next_integer_partition((5, 1, 1, 1)) == (4, 4)
    assert mathtools.next_integer_partition((4, 4)) == (4, 3, 1)


def test_mathtools_next_integer_partition_02():

    assert mathtools.next_integer_partition((4, 3, 1)) == (4, 2, 2)
    assert mathtools.next_integer_partition((4, 2, 2)) == (4, 2, 1, 1)
    assert mathtools.next_integer_partition((4, 2, 1, 1)) == (4, 1, 1, 1, 1)
    assert mathtools.next_integer_partition((4, 1, 1, 1, 1)) == (3, 3, 2)
    assert mathtools.next_integer_partition((3, 3, 2)) == (3, 3, 1, 1)
    assert mathtools.next_integer_partition((3, 3, 1, 1)) == (3, 2, 2, 1)
    assert mathtools.next_integer_partition((3, 2, 2, 1)) == (3, 2, 1, 1, 1)
