# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_partition_integer_into_halves_01():
    assert mathtools.partition_integer_into_halves(7, bigger='left') == (4, 3)
    assert mathtools.partition_integer_into_halves(7, bigger='right') == (3, 4)


def test_mathtools_partition_integer_into_halves_02():
    assert mathtools.partition_integer_into_halves(8, bigger='left') == (4, 4)
    assert mathtools.partition_integer_into_halves(8, bigger='right') == (4, 4)
    assert mathtools.partition_integer_into_halves(8, bigger='left', even='disallowed') == (5, 3)
    assert mathtools.partition_integer_into_halves(8, bigger='right', even='disallowed') == (3, 5)


def test_mathtools_partition_integer_into_halves_03():
    r'''Partition zero into halves.
    '''

    assert mathtools.partition_integer_into_halves(0, bigger='left') == (0, 0)
    assert mathtools.partition_integer_into_halves(0, bigger='right') == (0, 0)


def test_mathtools_partition_integer_into_halves_04():
    r'''Divide zero only into even halves.
    '''

    statement = "mathtools.partition_integer_into_halves(0, even='disallowed')"
    assert pytest.raises(PartitionError, statement)


def test_mathtools_partition_integer_into_halves_05():
    r'''Raise TypeError on noninteger n.
    Raise ValueError on negative n.
    '''

    statement = "mathtools.partition_integer_into_halves('foo')"
    assert pytest.raises(TypeError, statement)
    statement = 'mathtools.partition_integer_into_halves(-1)'
    assert pytest.raises(ValueError, statement)
