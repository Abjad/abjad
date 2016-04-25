# -*- coding: utf-8 -*-
import platform
import pytest
import sys
from abjad.tools import mathtools
from abjad.tools import systemtools


def test_mathtools_divisors_01():
    r'''Positive divisors of integer n.
    '''

    assert mathtools.divisors(1) == [1]
    assert mathtools.divisors(2) == [1, 2]
    assert mathtools.divisors(3) == [1, 3]
    assert mathtools.divisors(-4) == [1, 2, 4]
    assert mathtools.divisors(-5) == [1, 5]
    assert mathtools.divisors(-6) == [1, 2, 3, 6]
    assert mathtools.divisors(7) == [1, 7]
    assert mathtools.divisors(8) == [1, 2, 4, 8]
    assert mathtools.divisors(9) == [1, 3, 9]
    assert mathtools.divisors(10) == [1, 2, 5, 10]


def test_mathtools_divisors_02():
    r'''Raise not implemented error on zero.
    '''

    assert pytest.raises(NotImplementedError, 'mathtools.divisors(0)')


def test_mathtools_divisors_03():
    r'''Raise exception on noninteger n.
    '''

    assert pytest.raises(TypeError, 'mathtools.divisors(7.5)')


@pytest.mark.skipif(
    platform.python_implementation() != 'CPython',
    reason='Benchmarking is only for CPython.',
    )
def test_mathtools_divisors_04():
    r'''Performance is extremely fast.
    '''
    result = systemtools.IOManager.count_function_calls(
        'mathtools.divisors(100000000)',
        globals(),
        )
    if sys.version_info[0] == 2:
        assert result == 50
    else:
        assert result == 51
