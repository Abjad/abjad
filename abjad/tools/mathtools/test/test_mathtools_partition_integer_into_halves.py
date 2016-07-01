# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_partition_integer_into_halves_01():
    assert mathtools.partition_integer_into_halves(7, bigger=Left) == (4, 3)
    assert mathtools.partition_integer_into_halves(7, bigger=Right) == (3, 4)


def test_mathtools_partition_integer_into_halves_02():
    assert mathtools.partition_integer_into_halves(8, bigger=Left) == (4, 4)
    assert mathtools.partition_integer_into_halves(8, bigger=Right) == (4, 4)
    assert mathtools.partition_integer_into_halves(
        8, bigger=Left, even='disallowed') == (5, 3)
    assert mathtools.partition_integer_into_halves(
        8, bigger=Right, even='disallowed') == (3, 5)


def test_mathtools_partition_integer_into_halves_03():
    r'''Partition zero into halves.
    '''

    assert mathtools.partition_integer_into_halves(0, bigger=Left) == (0, 0)
    assert mathtools.partition_integer_into_halves(0, bigger=Right) == (0, 0)


def test_mathtools_partition_integer_into_halves_04():
    r'''Divide zero only into even halves.
    '''

    statement = "mathtools.partition_integer_into_halves(0, even='disallowed')"
    assert pytest.raises(Exception, statement)


def test_mathtools_partition_integer_into_halves_05():
    r'''Raises type error on noninteger n.
    Raises value error on negative n.
    '''

    statement = "mathtools.partition_integer_into_halves('foo')"
    assert pytest.raises(TypeError, statement)
    statement = 'mathtools.partition_integer_into_halves(-1)'
    assert pytest.raises(ValueError, statement)