from abjad import *
from abjad.tools import mathtools


def test_mathtools_partition_integer_into_thirds_01():
    '''Partition n into left, middle, right parts.'''

    #assert mathtools.partition_integer_into_thirds(0) == (0, 0, 0)
    assert mathtools.partition_integer_into_thirds(1) == (0, 1, 0)
    assert mathtools.partition_integer_into_thirds(2) == (1, 0, 1)
    assert mathtools.partition_integer_into_thirds(3) == (1, 1, 1)
    assert mathtools.partition_integer_into_thirds(4) == (1, 2, 1)
    assert mathtools.partition_integer_into_thirds(5) == (2, 1, 2)
    assert mathtools.partition_integer_into_thirds(6) == (2, 2, 2)
    assert mathtools.partition_integer_into_thirds(7) == (2, 3, 2)
    assert mathtools.partition_integer_into_thirds(8) == (3, 2, 3)
    assert mathtools.partition_integer_into_thirds(9) == (3, 3, 3)


def test_mathtools_partition_integer_into_thirds_02():
    '''Smallest part on left.'''

    #assert mathtools.partition_integer_into_thirds(
    #    0, smallest ='left') == (0, 0, 0)
    assert mathtools.partition_integer_into_thirds(
        1, smallest ='left') == (0, 1, 0)
    assert mathtools.partition_integer_into_thirds(
        2, smallest ='left') == (0, 1, 1)
    assert mathtools.partition_integer_into_thirds(
        3, smallest ='left') == (1, 1, 1)
    assert mathtools.partition_integer_into_thirds(
        4, smallest = 'left') == (1, 2, 1)
    assert mathtools.partition_integer_into_thirds(
        5, smallest = 'left') == (1, 2, 2)
    assert mathtools.partition_integer_into_thirds(
        6, smallest = 'left') == (2, 2, 2)
    assert mathtools.partition_integer_into_thirds(
        7, smallest = 'left') == (2, 3, 2)
    assert mathtools.partition_integer_into_thirds(
        8, smallest = 'left') == (2, 3, 3)
    assert mathtools.partition_integer_into_thirds(
        9, smallest = 'left') == (3, 3, 3)


def test_mathtools_partition_integer_into_thirds_03():
    '''Smallest part on right.'''

    #assert mathtools.partition_integer_into_thirds(0, smallest = 'right') == (0, 0, 0)
    assert mathtools.partition_integer_into_thirds(1, smallest = 'right') == (0, 1, 0)
    assert mathtools.partition_integer_into_thirds(2, smallest = 'right') == (1, 1, 0)
    assert mathtools.partition_integer_into_thirds(3, smallest = 'right') == (1, 1, 1)
    assert mathtools.partition_integer_into_thirds(4, smallest = 'right') == (1, 2, 1)
    assert mathtools.partition_integer_into_thirds(5, smallest = 'right') == (2, 2, 1)
    assert mathtools.partition_integer_into_thirds(6, smallest = 'right') == (2, 2, 2)
    assert mathtools.partition_integer_into_thirds(7, smallest = 'right') == (2, 3, 2)
    assert mathtools.partition_integer_into_thirds(8, smallest = 'right') == (3, 3, 2)
    assert mathtools.partition_integer_into_thirds(9, smallest = 'right') == (3, 3, 3)


def test_mathtools_partition_integer_into_thirds_04():
    '''Biggest part on left.'''

    #assert mathtools.partition_integer_into_thirds(0, biggest = 'left') == (0, 0, 0)
    assert mathtools.partition_integer_into_thirds(1, biggest = 'left') == (1, 0, 0)
    assert mathtools.partition_integer_into_thirds(2, biggest = 'left') == (1, 0, 1)
    assert mathtools.partition_integer_into_thirds(3, biggest = 'left') == (1, 1, 1)
    assert mathtools.partition_integer_into_thirds(4, biggest = 'left') == (2, 1, 1)
    assert mathtools.partition_integer_into_thirds(5, biggest = 'left') == (2, 1, 2)
    assert mathtools.partition_integer_into_thirds(6, biggest = 'left') == (2, 2, 2)
    assert mathtools.partition_integer_into_thirds(7, biggest = 'left') == (3, 2, 2)
    assert mathtools.partition_integer_into_thirds(8, biggest = 'left') == (3, 2, 3)
    assert mathtools.partition_integer_into_thirds(9, biggest = 'left') == (3, 3, 3)


def test_mathtools_partition_integer_into_thirds_05():
    '''Biggest part on right.'''

    #assert mathtools.partition_integer_into_thirds(0, biggest = 'right') == (0, 0, 0)
    assert mathtools.partition_integer_into_thirds(1, biggest = 'right') == (0, 0, 1)
    assert mathtools.partition_integer_into_thirds(2, biggest = 'right') == (1, 0, 1)
    assert mathtools.partition_integer_into_thirds(3, biggest = 'right') == (1, 1, 1)
    assert mathtools.partition_integer_into_thirds(4, biggest = 'right') == (1, 1, 2)
    assert mathtools.partition_integer_into_thirds(5, biggest = 'right') == (2, 1, 2)
    assert mathtools.partition_integer_into_thirds(6, biggest = 'right') == (2, 2, 2)
    assert mathtools.partition_integer_into_thirds(7, biggest = 'right') == (2, 2, 3)
    assert mathtools.partition_integer_into_thirds(8, biggest = 'right') == (3, 2, 3)
    assert mathtools.partition_integer_into_thirds(9, biggest = 'right') == (3, 3, 3)
