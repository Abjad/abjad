from abjad import *
from abjad.tools import mathtools


def test_mathtools_partition_integer_into_units_01():
    '''Partition integer n into n equal parts.
        Partition positive n into parts all equal to 1.'''

    t = mathtools.partition_integer_into_units(6)

    assert t == [1, 1, 1, 1, 1, 1]


def test_mathtools_partition_integer_into_units_02():
    '''Partition integer n into n equal parts.
        Partition negative n into parts all equal to -1.'''

    t = mathtools.partition_integer_into_units(-5)

    assert t == [-1, -1, -1, -1, -1]


def test_mathtools_partition_integer_into_units_03():
    '''Partition integer n into n equal parts.
        Return empty list when n is 0.'''

    t = mathtools.partition_integer_into_units(0)

    assert t == []
